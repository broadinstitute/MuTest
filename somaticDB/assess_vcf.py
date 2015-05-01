import argparse
import ast
from pymongo import MongoClient
from ConfusionMatrixManager import ConfusionMatrixManager
from DictUtilities import get_entries_from_dict, merge_dicts
import csv
from DataGatherer import DataGatherer
from ListUtilities import list_product_drop_none
from Variant import is_indel, is_snp, is_sv, get_variant_type



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

VARIANT_FIELDS=['chromosome','start','ref','alt','dataset_name','data_subset_name']

test_data_set  = {}
truth_data_set = {}
false_data_set = {}

missed_positives     = set([])
discovered_negatives = set([])

gather = DataGatherer(args.input)

for variant_dict in gather.data_iterator(keys=['dataset_name','data_subset_name','data_filename']):
    variant_data = get_entries_from_dict(variant_dict, keys=VARIANT_FIELDS,return_type=tuple)

    print variant_dict['FILTER']

    if variant_dict.has_key('FILTER'):
        if (variant_dict['FILTER'] != '.')&(variant_dict['FILTER'] != 'PASS'):
            continue

    test_data_set[variant_data] = get_variant_type(variant_dict)

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

    if evidence_type == 'TP': truth_data_set[confirmation_data_tuple] = get_variant_type(record)
    if evidence_type == 'FP': false_data_set[confirmation_data_tuple] = get_variant_type(record)

all_variants = merge_dicts(truth_data_set,false_data_set,test_data_set)

print list(truth_data_set)[:10]
print list(false_data_set)[:10]
print list(test_data_set)[:10]

def save_set(filename = "", header=None, data=""):
    data = list(data)

    file = open(filename,'w')
    writer = csv.DictWriter(file, fieldnames=header, delimiter='\t')

    for row in data:
        writer.writerow(dict(zip(header,row)))

    file.close()



for variant in all_variants:
    false_positive = variant in false_data_set
    true_positive = variant in truth_data_set
    submitted = variant in test_data_set

    dataset, data_subset = variant[4:]

    variant_categories = list_product_drop_none((dataset,(dataset, data_subset)),
                                                (None, all_variants[variant]))

    if true_positive:
        if submitted:
            ConfusionDataTPs.add(keys=variant_categories,
                                 test=True,
                                 truth=True)
        else:
            ConfusionDataTPs.add(keys=variant_categories,
                                 test=False,
                                 truth=True)
            missed_positives.add(variant)
    else:
        if submitted:
            ConfusionDataTPs.add(keys=variant_categories,
                                 test=True,
                                 truth=False)

    if false_positive:
        if submitted:
            ConfusionDataFPs.add(keys=variant_categories,
                                 test=True,
                                 truth=False)
            discovered_negatives.add(variant)
        else:
            ConfusionDataFPs.add(keys=variant_categories,
                                 test=False,
                                 truth=False)
    else:
        if submitted:
            ConfusionDataFPs.add(keys=variant_categories,
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