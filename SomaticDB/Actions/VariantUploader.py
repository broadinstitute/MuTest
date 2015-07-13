from SomaticDB.BasicUtilities.DictUtilities import merge_dicts , \
    get_entries_from_dict
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import DataGatherer
from SomaticDB.SupportLibraries.SomaticFileSystem import SomaticFileSystem
import time
import os
from SomaticDB.SupportLibraries.SubmissionFile import SubmissionFile

script_description="""A protype script for submitting data to MongoDB"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """


def change_data_filename(directory,filename):
    return os.path.join(directory,os.path.basename(filename))

def VariantUploader(tsv,submit_to_filesystem=False):


    gather = DataGatherer(tsv)

    variants = connect_to_mongo()

    if submit_to_filesystem:
        filesystem = SomaticFileSystem('/dsde/working/somaticDB/master/data')

        S = SubmissionFile(tsv)
        S.change_file_dir()
        S.to_csv(os.path.join('/dsde/working/somaticDB/master/records',os.path.basename(tsv)))
    else:
        filesystem = None


    bulk_count = 0
    bulk = variants.initialize_unordered_bulk_op()

    start_time = time.time()
    n = 0

    for variant_dict in gather.data_iterator():
        n+=1


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


        if filesystem:
            project = mongo_submission['project']
            dataset = mongo_submission['dataset']
            filesystem.add_project(project)
            filesystem[project].add_dataset(dataset)

            filesystem[project][dataset].add_file(mongo_submission['data_filename'])

            mongo_submission['data_filename']=\
                change_data_filename("/dsde/working/somaticDB/master/data/%s/%s/"%(project,dataset),
                                     mongo_submission['data_filename'])




        bulk.insert(mongo_submission)

        if bulk_count == 10000:
            print "variants uploaded: %d (%.2f seconds since start of upload)." % (n, time.time() - start_time)
            bulk_count = 0
            bulk.execute()
            bulk = variants.initialize_unordered_bulk_op()

    if bulk_count>0:
        print "variants uploaded: %d (%.2f seconds since start of upload)." % (n, time.time() - start_time)
        bulk.execute()