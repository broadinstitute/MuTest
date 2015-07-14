import argparse
from SomaticDB.BasicUtilities.DictUtilities import merge_dicts , \
    get_entries_from_dict
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import DataGatherer


script_description="""A protype script for submitting data to MongoDB"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

def VariantUploader(tsv):

    filename = tsv

    gather = DataGatherer(filename)

    variants = connect_to_mongo()


    bulk_count = 0
    bulk = variants.initialize_unordered_bulk_op()

    for variant_dict in gather.data_iterator(demo=False):

        bulk_count+=1

        additional_data_dict={}

        mongo_submission = merge_dicts(variant_dict, additional_data_dict)

        unique_data = get_entries_from_dict(mongo_submission, keys=['chromosome',
                                                                    'start',
                                                                    'ref',
                                                                    'alt',
                                                                    'dataset_name',
                                                                    'data_subset_name',
                                                                    'evidence_type'],
                                            return_type=dict)



        bulk.insert(unique_data)

        if bulk_count == 10000:
            print "bulk upload."
            bulk_count = 0
            bulk.execute()
            bulk = variants.initialize_unordered_bulk_op()
