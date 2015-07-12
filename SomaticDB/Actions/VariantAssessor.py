import ast
import csv
from SomaticDB.SupportLibraries.ConfusionMatrixManager import \
    ConfusionMatrixManager
from SomaticDB.SupportLibraries.Variant import get_variant_type

import argparse
from SomaticDB.BasicUtilities.DictUtilities import get_entries_from_dict , \
    merge_dicts
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import DataGatherer , \
    query_processor


def pp_dict(x):
    for key in x.keys():
        print key+": "+str(x[key])




script_description="""A protype script that accesses true and false positives"""
script_epilog="""Created for evaluation of performance of Mutect 2 """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)




def VariantAssessor(query,tsv):

    collection = connect_to_mongo()

    VARIANT_FIELDS=['chromosome','start','ref','alt','dataset_name','data_subset_name']

    test_data_set  = {}
    truth_data_set = {}
    false_data_set = {}

    missed_positives     = set([])
    discovered_negatives = set([])

    gather = DataGatherer(tsv)

    for variant_dict in gather.data_iterator(keys=['dataset_name','data_subset_name','data_filename']):
        variant_data = get_entries_from_dict(variant_dict, keys=VARIANT_FIELDS,return_type=tuple)

        test_data_set[variant_data] = get_variant_type(variant_dict)

    ConfusionDataTPs = ConfusionMatrixManager()
    ConfusionDataFPs = ConfusionMatrixManager()

    query = query_processor(query)

    for record in collection.find(ast.literal_eval(query)):

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

        project, dataset = variant[4:]

        variant_categories = {project,(project, dataset)}

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
                print "fp:", variant, all_variants[variant]

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

    save_set(filename = "missed_true_positives.tsv",
             header=VARIANT_FIELDS,
             data = missed_positives)

    save_set(filename = "discovered_false_positives.tsv",
             header=VARIANT_FIELDS,
             data = discovered_negatives)

    CONFUSION_FIELDS = ['true positives','false positives','true negatives',
                        'false negatives','sensitivity','specificity',
                        'precision','false discovery rate','MCC']

    ConfusionDataFPs.save(filename="confusion_matrix_false_positives.tsv",
                          fieldnames=CONFUSION_FIELDS)

    ConfusionDataTPs.save(filename="confusion_matrix_true_positives.tsv",
                          fieldnames=CONFUSION_FIELDS)