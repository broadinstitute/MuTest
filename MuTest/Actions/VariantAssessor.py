import ast
import os
from collections import defaultdict
from MuTest.BasicUtilities.DictUtilities import get_entries_from_dict , \
    merge_dicts
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.DataGatherer import DataGatherer , \
    query_processor
import pandas as pd
import numpy as np

import logging
from MuTest.SupportLibraries.Variant import is_snp , is_indel

import csv

def pp_dict(x):
    for key in x.keys():
        print key+": "+str(x[key])


def VariantAssessor(query,tsv,output_file,outdir=""):

    collection = connect_to_mongo()

    caller_output = pd.read_csv(tsv,sep='\t')

    known_true     = {'snp': defaultdict(set),'indel': defaultdict(set)}
    known_false    = {'snp': defaultdict(set),'indel': defaultdict(set)}
    found_variants = {'snp': defaultdict(set),'indel': defaultdict(set)}

    false_positive = {'snp': defaultdict(set),'indel': defaultdict(set)}

    query = query_processor(query)

    logging.getLogger(__name__).info("Querying database for variants.")

    # collect query information
    for record in collection.find(ast.literal_eval(query)):

        sample_information = get_entries_from_dict(record, keys=['project','dataset','sample'],return_type=tuple)
        variant = get_entries_from_dict(record, keys=['chromosome','start','ref','alt'],return_type=tuple)

        sample_information = tuple(map(str, sample_information))
        variant = tuple(map(str, variant))

        evidence_type = record['evidence_type']

        if is_snp(record):
            if 'TP' in evidence_type:
                known_true['snp'][sample_information].add(variant)

            if 'FP' in evidence_type:
                known_false['snp'][sample_information].add(variant)

        elif is_indel(record):
            if 'TP' in evidence_type:
                known_true['indel'][sample_information].add(variant)

            if 'FP' in evidence_type:
                known_false['indel'][sample_information].add(variant)

    normal_normal = set([])
    cm = set([])

    #index the type of assessment to be done for each datatype.
    for k,row in caller_output.iterrows():
        sample_information = (row['project'],row['dataset'],row['sample'])
        if row['evidence_type'] == 'NN':
            normal_normal.add(sample_information)
        elif row['evidence_type'] == 'CM':
            cm.add(sample_information)
        else:
            cm.add(sample_information) #by default, ROC-like curves are used.

    gather = DataGatherer(tsv)


    logging.getLogger(__name__).info("Collection of variants from user submitted files.")

    found_feature_data = defaultdict(dict)

    #data from file (algorithm being tested)
    for variant_dict in gather.data_iterator():
        sample_information = get_entries_from_dict(variant_dict, keys=['project','dataset','sample'],return_type=tuple)
        variant = get_entries_from_dict(variant_dict, keys=['chromosome','start','ref','alt'],return_type=tuple)

        print sample_information, variant

        #found_feature_data[sample_information][variant] = get_entries_from_dict(variant_dict, keys=['ECNT','HCNT','NLOD','TLOD'],return_type=dict)

        if is_snp(variant_dict):
                found_variants['snp'][sample_information].add(variant)



        elif is_indel(variant_dict):
                found_variants['indel'][sample_information].add(variant)

    #print found_feature_data.keys()

    caller_samples = caller_output[['project','dataset','sample']].values.tolist()

    data = []

    for feature in ['snp','indel']:

        filename = {}; fp_fn = {}; fp_fp={}; all_dict={}; fp_tp= {}

        filename[feature] = feature+".false_negatives.tsv"
        fp_fn[feature] = csv.DictWriter(open( os.path.join(outdir,filename[feature])  ,'w'),
                                        delimiter='\t',
                                        fieldnames=['project','dataset','sample','chromosome','start','ref','alt','variant_type'])


        #fieldnames=['project','dataset','sample','chromosome','start','ref','alt','ECNT','HCNT','NLOD','TLOD','variant_type']
        fieldnames=['project','dataset','sample','chromosome','start','ref','alt','variant_type']
        filename[feature] = feature+".false_positives.tsv"
        fp_fp[feature] = csv.DictWriter(open( os.path.join(outdir,filename[feature]) ,'w'),
                                        delimiter='\t',
                                        fieldnames=fieldnames)


        #fieldnames=['project','dataset','sample','chromosome','start','ref','alt','ECNT','HCNT','NLOD','TLOD','variant_type']
        fieldnames=['project','dataset','sample','chromosome','start','ref','alt','variant_type']
        filename[feature] = feature+".true_positives.tsv"
        fp_tp[feature] = csv.DictWriter(open( os.path.join(outdir,filename[feature]) ,'w'),
                                        delimiter='\t',
                                        fieldnames=fieldnames)


        fp_fn[feature].writeheader()
        fp_fp[feature].writeheader()
        fp_tp[feature].writeheader()


        for eval_type in ['CM','NN']:

            all_dict[eval_type] = {'project': 'all',
                                   'dataset': 'all',
                                   'sample' : 'all',
                                   'false_positives': 0,
                                   'true_positives':  0,
                                   'false_negatives': 0,
                                   'tpr': np.nan,
                                   'fpr': np.nan,
                                   'precision': np.nan,
                                   'evidence_type': eval_type,
                                   'variant_type': feature }


        for sample_information in map(tuple,caller_samples):

            if sample_information in normal_normal:
                assessment_type = 'NN'
            elif sample_information in cm:
                assessment_type = 'CM'
            else:
                assessment_type = 'CM'



            row_dict = {'project': sample_information[0],
                        'dataset': sample_information[1],
                        'sample' : sample_information[2],
                        'false_positives': 0,
                        'true_positives': 0,
                        'false_negatives': 0,
                        'tpr': np.nan,
                        'fpr': np.nan,
                        'precision': np.nan,
                        'evidence_type': assessment_type,
                        'variant_type': feature}

            if assessment_type == 'NN':

                FN = len(found_variants[feature][sample_information])
                row_dict['false_positives'] = FN
                row_dict['precision'] = 0

            if assessment_type == 'CM':

                TP = np.float(len(found_variants[feature][sample_information].intersection(known_true[feature][sample_information])))
                FN = np.float(len(known_true[feature][sample_information].difference(found_variants[feature][sample_information])))
                FP = np.float(len(found_variants[feature][sample_information].difference(known_true[feature][sample_information])))

                print TP, FN, FP

                try:
                    row_dict['tpr']  = TP/(TP+FN)
                except:
                    row_dict['tpr']  = np.nan


                row_dict['true_positives']  = TP
                row_dict['false_negatives'] = FN
                row_dict['false_positives'] =  FP

                all_dict['CM']['true_positives']  += TP
                all_dict['CM']['false_negatives'] += FN
                all_dict['CM']['false_positives'] +=  FP

                try:
                    row_dict['precision'] = TP/(TP+FP)
                except:
                    row_dict['precision']  = np.nan

                row_dict['dream_accuracy'] = (row_dict['tpr'] + row_dict['precision'])/2.0

                print row_dict['tpr'], row_dict['precision'], row_dict['dream_accuracy']

                row_dict['variant_type'] = feature

            data.append(row_dict)



            true_positives  = list(found_variants[feature][sample_information].intersection(known_true[feature][sample_information]))
            false_positives = list(found_variants[feature][sample_information].difference(known_true[feature][sample_information]))
            false_negatives = list(known_true[feature][sample_information].difference(found_variants[feature][sample_information]))

            for variant in true_positives:

                fp_tp[feature].writerow({'project': sample_information[0],
                                         'dataset':sample_information[1],
                                         'sample':sample_information[2],
                                         'chromosome':variant[0],
                                         'start':variant[1],
                                         'ref':variant[2],
                                         'alt':variant[3],
                                         #'ECNT':found_feature_data[sample_information][variant]['ECNT'],
                                         #'HCNT':found_feature_data[sample_information][variant]['HCNT'],
                                         #'NLOD':found_feature_data[sample_information][variant]['NLOD'],
                                         #'TLOD':found_feature_data[sample_information][variant]['TLOD'],
                                         'variant_type':feature})

            for variant in false_positives:

                fp_fp[feature].writerow({'project': sample_information[0],
                                         'dataset':sample_information[1],
                                         'sample':sample_information[2],
                                         'chromosome':variant[0],
                                         'start':variant[1],
                                         'ref':variant[2],
                                         'alt':variant[3],
                                         #'ECNT':found_feature_data[sample_information][variant]['ECNT'],
                                         #'HCNT':found_feature_data[sample_information][variant]['HCNT'],
                                         #'NLOD':found_feature_data[sample_information][variant]['NLOD'],
                                         #'TLOD':found_feature_data[sample_information][variant]['TLOD'],
                                         'variant_type':feature})

            for variant in false_negatives:

                fp_fn[feature].writerow({'project': sample_information[0],
                                          'dataset':sample_information[1],
                                          'sample':sample_information[2],
                                          'chromosome':variant[0],
                                          'start':variant[1],
                                          'ref':variant[2],
                                          'alt':variant[3],
                                          'variant_type':feature})



        try:
            all_dict['CM']['tpr'] = all_dict['CM']['true_positives']/(all_dict['CM']['true_positives']+all_dict['CM']['false_negatives'])
        except:
            all_dict['CM']['tpr'] = np.nan


        all_dict['CM']['dream_accuracy'] = (all_dict['CM']['tpr'] + 1 -all_dict['CM']['precision'])/2.0

        try:
            all_dict['CM']['precision'] = all_dict['CM']['true_positives']/(all_dict['CM']['true_positives']+all_dict['CM']['false_positives'])
        except:
            all_dict['CM']['precision'] = np.nan



        all_dict['CM']['dream_accuracy'] = (all_dict['CM']['tpr'] + all_dict['CM']['precision'])/2.0

        all_dict['CM']['variant_type'] = feature

        #data.append(all_dict['CM'])
        #data.append(all_dict['NN'])

    fieldnames=['project','dataset','sample' ,'false_positives','true_positives','false_negatives','tpr','precision','evidence_type','dream_accuracy','variant_type']

    pd.DataFrame(data).to_csv(output_file, sep='\t',index=False,columns=fieldnames,na_rep='nan')