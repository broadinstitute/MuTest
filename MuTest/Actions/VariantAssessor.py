import ast
from collections import defaultdict
from MuTest.BasicUtilities.DictUtilities import get_entries_from_dict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.DataGatherer import DataGatherer , \
    query_processor
import pandas as pd
import numpy as np

def pp_dict(x):
    for key in x.keys():
        print key+": "+str(x[key])


def save_set(fp,list_data):

    list_data = list(list_data)
    for entry in list_data:
        fp.write("\t".join(entry)+"\n")



def VariantAssessor(query,tsv,output_file):

    collection = connect_to_mongo()

    caller_output = pd.read_csv(tsv,sep='\t')

    known_true     = defaultdict(set)
    known_false    = defaultdict(set)
    found_variants = defaultdict(set)

    false_positive = defaultdict(int)

    query = query_processor(query)

    # collect query information
    for record in collection.find(ast.literal_eval(query)):

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
        if row['evidence_type'] == 'NN':
            normal_normal.add(sample_information)
        elif row['evidence_type'] == 'CM':
            cm.add(sample_information)
        else:
            roc_like.add(sample_information) #by default, ROC-like curves are used.

    gather = DataGatherer(tsv)

    #data from file (algorithm being tested)
    for variant_dict in gather.data_iterator():
        sample_information = get_entries_from_dict(variant_dict, keys=['project','dataset','sample'],return_type=tuple)
        variant = get_entries_from_dict(variant_dict, keys=['chromosome','start','ref','alt'],return_type=tuple)


        if sample_information in roc_like:
            found_variants[sample_information].add(variant)

        if sample_information in cm:
            found_variants[sample_information].add(variant)

        if sample_information in normal_normal:
            false_positive[sample_information]+=1


    caller_samples = caller_output[['project','dataset','sample']].values.tolist()

    data = []


    filename = "missed_positives.tsv"
    fp = open(filename,'w')
    fp.write("\t".join(['chromosome','start','ref','alt'])+'\n')


    all_dict = {'project': 'all',
                'dataset': 'all',
                'sample' : 'all',
                'false_positives': 0,
                'true_positives':  0,
                'false_negatives': 0,
                'tpr': np.nan,
                'fpr': np.nan,
                'precision': np.nan,
                'evidence_type': 'CM' }

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
                    'tpr': np.nan,
                    'fpr': np.nan,
                    'precision': np.nan,
                    'evidence_type': assessment_type }

        if assessment_type == 'NN':
            row_dict['false_positives'] = false_positive

        if assessment_type == 'CM':
            print 'found:'
            print found_variants[sample_information]
            print len(found_variants[sample_information])
            print 'known:'
            print known_true[sample_information]
            print len(known_true[sample_information])
            print
            print sample_information
            print
            print

            TP = np.float(len(found_variants[sample_information].intersection(known_true[sample_information])))
            FN = np.float(len(known_true[sample_information].difference(found_variants[sample_information])))
            FP = np.float(len(found_variants[sample_information].difference(known_true[sample_information])))

            print TP, FN, FP

            try:
                row_dict['tpr']  = TP/(TP+FN)
            except:
                row_dict['tpr']  = np.nan


            row_dict['true_positives']  = TP
            row_dict['false_negatives'] = FN
            row_dict['false_positives'] =  FP

            all_dict['true_positives']  += TP
            all_dict['false_negatives'] += FN
            all_dict['false_positives'] +=  FP

            row_dict['precision'] = TP/(TP+FP)

            row_dict['dream_accuracy'] = (row_dict['tpr'] + 1 -row_dict['precision'])/2.0

            print row_dict['tpr'], row_dict['precision'], row_dict['dream_accuracy']


        data.append(row_dict)

        save_set(fp,list(known_true[sample_information].difference(found_variants[sample_information])))

    all_dict['tpr'] = all_dict['true_positives']/(all_dict['true_positives']+all_dict['false_negatives'])
    all_dict['dream_accuracy'] = (all_dict['tpr'] + 1 -all_dict['precision'])/2.0
    all_dict['precision'] = all_dict['true_positives']/(all_dict['true_positives']+all_dict['false_positives'])

    data.append(all_dict)

    print data

    fp.close()
    fieldnames=['project','dataset','sample' ,'false_positives','true_positives','false_negatives','tpr','fpr','precision','evidence_type','dream_accuracy']

    pd.DataFrame(data).to_csv(output_file, sep='\t',index=False,columns=fieldnames)