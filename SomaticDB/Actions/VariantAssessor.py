import ast
from collections import defaultdict
import csv
from SomaticDB.SupportLibraries.ConfusionMatrix import ConfusionMatrix
from SomaticDB.BasicUtilities.DictUtilities import get_entries_from_dict , \
    merge_dicts
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import DataGatherer , \
    query_processor
import pandas as pd
import numpy as np
import collections

def pp_dict(x):
    for key in x.keys():
        print key+": "+str(x[key])


def save_set(filename,list_data,header=None):
    file = open(filename)

    if header is not None:
        file.write("\t".join(header)+"\n")

    list_data = list(list_data)
    for entry in list_data:
        file.write("\t".join(entry)+"\n")
    file.close()


def VariantAssessor(query,tsv,output_file):

    collection = connect_to_mongo()

    caller_output = pd.read_csv(tsv,sep='\t')

    known_true     = defaultdict(set)
    known_false    = defaultdict(set)
    found_variants = defaultdict(set)

    false_positive = defaultdict(int)

    query = query_processor(query)

    # collect query information
    for record in collections.find(ast.literal_eval(query)):

        sample_information = get_entries_from_dict(record, keys=['project','dataset','sample'],return_type=tuple)
        variant = get_entries_from_dict(record, keys=['chromosome','start','ref','alt'],return_type=tuple)

        sample_information = tuple(map(str, sample_information))
        variant = tuple(map(str, variant))

        evidence_type = record['evidence_type']

        if 'TP' in evidence_type:
            known_true[sample_information].add(variant)

        if 'FP' in evidence_type:
            known_false[sample_information].add(variant)


    roc_like = set([])
    normal_normal = set([])
    cm = set([])

    #index the type of assessment to be done for each datatype.
    for k,row in caller_output.iterrows():
        sample_information = (row['project'],row['dataset'],row['sample'])
        if row['assessment_type'] == 'ROCL':
            roc_like.add(sample_information)
        elif row['assessment_type'] == 'NN':
            normal_normal.add(sample_information)
        elif row['assessment_type'] == 'CM':
            cm.add(sample_information)
        else:
            roc_like.add(sample_information) #by default, ROC-like curves are used.

    gather = DataGatherer(tsv)

    #data from file (algorithm being tested)
    for variant_dict in gather.data_iterator():
        sample_information = get_entries_from_dict(variant_dict, keys=['project','dataset','sample'],return_type=tuple)
        variant = get_entries_from_dict(variant_dict, keys=['chromosome','start','ref','alt'],return_type=tuple)

        if sample_information in roc_like:
            if 'TP' in variant_dict['evidence_type']: found_variants[sample_information].add(variant)

        if sample_information in cm:
            if 'TP' in variant_dict['evidence_type']: found_variants[sample_information].add(variant)

        if sample_information in normal_normal:
            false_positive[sample_information]+=1


    caller_samples = caller_output[['project','dataset','sample']].values.tolist()

    data = []

    for sample_information in map(tuple,caller_samples):

        if sample_information in roc_like:
            assessment_type = 'ROCL'
        elif sample_information in normal_normal:
            assessment_type = 'NN'
        elif sample_information in cm:
            assessment_type = 'CM'
        else:
            assessment_type = 'ROCL'


        row_dict = {'project': sample_information[0],
                    'dataset': sample_information[1],
                    'sample' : sample_information[2],
                    'false_positives': np.nan,
                    'true_positives': np.nan,
                    'tpr': np.nan,
                    'fpr': np.nan,
                    'precision': np.nan,
                    'assessment_type': assessment_type }

        if assessment_type == 'NN':
            row_dict['false_positives'] = false_positive

        if assessment_type == 'ROCL':
            TP = len(found_variants.intersection(known_true))
            FN = len(known_true.difference(found_variants))

            row_dict['tpr']  = TP/(TP+FN)

            row_dict['true_positives'] = TP

            FP = found_variants.intersection(known_false)
            TN = known_false.difference(found_variants)

            row_dict['fpr']  = FP/(FP+TN)

            row_dict['false_positives'] = FP

        if assessment_type == 'CM':
            TP = len(found_variants.intersection(known_true))
            FP = len(found_variants.different(known_true))
            FN = len(known_true.difference(found_variants))

            row_dict['true_positives'] = TP
            row_dict['false_positives'] = FP

            row_dict['tpr']  = TP/(TP+FN)
            row_dict['precision'] = TP/(TP+TP)

        data.append(row_dict)


        filename = "-".join(sample_information)+".missed_positives.tsv"
        save_set(filename,list(known_true.difference(found_variants)),header=['chromosome','start','ref','alt'])

        pd.DataFrame(data).to_csv(output_file, sep='\t')
