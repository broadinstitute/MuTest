import argparse
from DataGatherer import DataGatherer
from DictUtilities import merge_dicts , get_entries_from_dict
from MongoUtilities import connect_to_mongo


script_description="""A protype script for submitting data to MongoDB"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                description=script_description,
                                epilog=script_epilog,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)

args = parser.parse_args()

filename = args.tsv

gather = DataGatherer(filename)

variants = connect_to_mongo()


bulk_count = 0
bulk = variants.initialize_unordered_bulk_op()


for variant_dict in gather.data_iterator(demo=args.demo):

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
