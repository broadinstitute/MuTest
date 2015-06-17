
import csv
import argparse
import datetime
from pymongo import MongoClient
from DictUtilities import merge_dicts
from DatabaseParser import DatabaseParser
from DictUtilities import get_entries_from_dict


class DataGatherer:
    def __init__(self, filename):
        self.filename = filename

    def data_iterator(self, demo=False,keys=('tumor_bam',
                                             'normal_bam',
                                             'data_filename',
                                             'dataset_name',
                                             'data_subset_name',
                                             'evidence_type')):
        file = open(self.filename,'rU')
        reader = csv.DictReader(file,delimiter='\t')

        for file_data in reader:

            print "submitting:"
            print "\tdataset:", file_data['dataset_name']
            print "\tsubset:", file_data['data_subset_name']
            if file_data.has_key('evidence_type'): print "\tevidence type", file_data['evidence_type']
            print

            meta_data_dict = get_entries_from_dict(file_data,
                                                   keys=keys,
                                                   return_type=dict)

            D = DatabaseParser(meta_data_dict['data_filename'])

            n=0
            for variant_dict in D.get_variants():
                n+=1
                if demo:
                    if (n > 50): break
                yield merge_dicts(variant_dict, meta_data_dict)


def main():
    script_description="""A protype script for submitting data to MongoDB"""
    script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                    description=script_description,
                                    epilog=script_epilog,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('-i','--input', help='Input file name',type=str,metavar='<input_file>', default="ALL",required=True)
    parser.add_argument('-p','--port', help='Input file name',type=int,metavar='<input_file>', default=27017)
    parser.add_argument('-d','--demo', help='Demo mode',action='store_true')

    args = parser.parse_args()

    filename = args.input
    if filename == "DEFAULT": filename = "/dsde/working/somaticDB/master/tcga/submission_data.tsv"

    gather = DataGatherer(filename)

    client = MongoClient('104.197.21.136', args.port )
    client.somatic_db_master.authenticate('kareem', 'p1IU5lec5WM7NeA')
    db = client['somatic_db_master']
    collection = db['ValidationData']


    bulk_count = 0
    bulk = collection.initialize_unordered_bulk_op()


    for variant_dict in gather.data_iterator(demo=args.demo):

        bulk_count+=1


        additional_data_dict={} #{'submission_time': str(datetime.datetime.utcnow())}

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
            bulk = collection.initialize_unordered_bulk_op()



if __name__ == "__main__":
    main()