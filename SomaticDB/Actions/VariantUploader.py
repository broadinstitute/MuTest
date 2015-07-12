import argparse
from SomaticDB.BasicUtilities.DictUtilities import merge_dicts , \
    get_entries_from_dict
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import DataGatherer
from SomaticDB.SupportLibraries.SomaticFileSystem import SomaticFileSystem


script_description="""A protype script for submitting data to MongoDB"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

def VariantUploader(tsv,submit_to_filesystem=False):

    filename = tsv

    gather = DataGatherer(filename)

    variants = connect_to_mongo()

    if submit_to_filesystem:
        filesystem = SomaticFileSystem('/dsde/working/somaticDB/master')
    else:
        filesystem = None


    bulk_count = 0
    bulk = variants.initialize_unordered_bulk_op()

    for variant_dict in gather.data_iterator():

        bulk_count+=1

        additional_data_dict={}

        mongo_submission = merge_dicts(variant_dict, additional_data_dict)

        unique_data = get_entries_from_dict(mongo_submission, keys=['chromosome',
                                                                    'start',
                                                                    'ref',
                                                                    'alt',
                                                                    'project',
                                                                    'dataset',
                                                                    'evidence_type'],
                                            return_type=dict)

        project = mongo_submission['project']
        dataset = mongo_submission['dataset']


        filesystem.add_project(project)
        filesystem[project].add_dataset(dataset)
        filesystem[project][dataset].add_file(  )


        bulk.insert(mongo_submission)

        if bulk_count == 10000:
            print "bulk upload."
            bulk_count = 0
            bulk.execute()
            bulk = variants.initialize_unordered_bulk_op()
