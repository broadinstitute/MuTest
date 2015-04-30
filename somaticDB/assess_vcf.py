import argparse
import ast
from pymongo import MongoClient
from ConfusionMatrixManager import ConfusionMatrixManager
from DatabaseParser import DatabaseParser
from DictUtilities import get_entries_from_dict
import csv
from DataGatherer import DataGatherer


def pp_dict(x):
    for key in x.keys():
        print key+": "+str(x[key])


script_description="""A protype script that accesses true and false positives"""
script_epilog="""Created for evaluation of performance of Mutect 2 """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i','--input', help='The file to be assessed',type=str,metavar='<input_file>', required=True)
parser.add_argument('-q','--query', help='The query for the dataset needed',type=str,metavar='<query>', required=True)
parser.add_argument('-s','--algorithm', help='The name of the submission',type=str,metavar='<algorithm_name>', required=True)
parser.add_argument('-v','--version', help='The name of the submission',type=str,metavar='<algorithm_name>')

args = parser.parse_args()

client = MongoClient('localhost', 27017)
db = client['SomaticMutations']
collection = db['ValidationData']

VARIANT_FIELDS=['chromosome','start','ref','alt','dataset','data_subset']

test_data_set = set([])
truth_data_set = set([])
false_data_set = set([])

missed_positives     = set([])
discovered_negatives = set([])

gather = DataGatherer(args.input)



for variant_dict in gather.data_iterator(keys=['dataset_name','data_subset_name','data_filename']):
    variant_data = get_entries_from_dict(variant_dict, keys=VARIANT_FIELDS,return_type=list)
    test_data_set.add(variant_data)

data_collection=[]

ConfusionDataTPs = ConfusionMatrixManager()
ConfusionDataFPs = ConfusionMatrixManager()

for record in collection.find(ast.literal_eval(args.query)):

    confirmation_data_list =\
        get_entries_from_dict(record,
                              keys=VARIANT_FIELDS,
                              return_type=list)

    confirmation_data_tuple = tuple(map(str, confirmation_data_list))

    evidence_type = record['evidence_type']

    if evidence_type == 'TP': truth_data_set.add(confirmation_data_tuple)
    if evidence_type == 'FP': false_data_set.add(confirmation_data_tuple)

all_variants = set.union(truth_data_set,false_data_set,test_data_set)


def save_set(filename = "", header=None, data=""):
    data = list(data)

    file = open(filename)
    writer = csv.DictWriter(file, fieldnames=header, delimiter='\t')

    for row in data:
        writer.writerow(dict(zip(header,row)))

    file.close()



for variant in all_variants:
    false_positive = variant in false_data_set
    true_positive = variant in truth_data_set
    submitted = variant in test_data_set

    dataset, data_subset = variant[4:]

    if true_positive:
        if submitted:
            ConfusionDataTPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=True,
                                 truth=True)
        else:
            ConfusionDataTPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=False,
                                 truth=True)
            missed_positives.add(variant)
    else:
        if submitted:
            ConfusionDataTPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=True,
                                 truth=False)

    if false_positive:
        if submitted:
            ConfusionDataFPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=True,
                                 truth=False)
            discovered_negatives.add(variant)
        else:
            ConfusionDataFPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=False,
                                 truth=False)
    else:
        if submitted:
            ConfusionDataFPs.add(keys=[dataset,(dataset, data_subset)],
                                 test=True,
                                 truth=True)

save_set(filename = "%s.%s.missed_true_positives.tsv" %(args.algorithm,args.version),
         header=VARIANT_FIELDS,
         data = missed_positives)

save_set(filename = "%s.%s.discovered_false_positives.tsv" %(args.algorithm,args.version),
         header=VARIANT_FIELDS,
         data = discovered_negatives)

CONFUSION_FIELDS = ['true positives','false positives','true negatives',
                    'false negatives','sensitivity','specificity',
                    'precision','false discovery rate']

ConfusionDataFPs.save(filename="%s.%s.confusion_matrix_false_positives.tsv" %(args.algorithm,args.version),
                      fieldnames=CONFUSION_FIELDS)

ConfusionDataTPs.save(filename="%s.%s.confusion_matrix_true_positives.tsv" %(args.algorithm,args.version),
                      fieldnames=CONFUSION_FIELDS)