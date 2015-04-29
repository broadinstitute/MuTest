
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

    def data_iterator(self):
        file = open(self.filename,'rU')
        reader = csv.DictReader(file,delimiter='\t')

        for file_data in reader:

            print "submitting:"
            print "\tdataset:", file_data['dataset_name']
            print "\tsubset:", file_data['data_subset_name']
            print "\tevidence type", file_data['evidence_type']
            print

            meta_data_dict = get_entries_from_dict(file_data,

                                                   keys=['tumor_bam',
                                                         'normal_bam',
                                                         'data_filename',
                                                         'dataset_name',
                                                         'data_subset_name',
                                                         'evidence_type'],

                                                   return_type=dict)

            D = DatabaseParser(meta_data_dict['data_filename'])

            n=0
            for variant_dict in D.get_variants():
                n+=1
                if (n > 100): break
                yield merge_dicts(variant_dict, meta_data_dict)

            break


def main():
    script_description="""A protype script for submitting data to MongoDB"""
    script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                    description=script_description,
                                    epilog=script_epilog,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('-i','--input', help='Input file name',type=str,metavar='<input_file>', default="ALL",required=True)
    parser.add_argument('-p','--port', help='Input file name',type=int,metavar='<input_file>', default=27017)

    args = parser.parse_args()

    filename = args.input
    if filename == "ALL": filename = "../data/submission_data.tsv"

    gather = DataGatherer(filename)

    client = MongoClient('localhost', args.port )
    db = client['SomaticMutations']
    collection = db['ValidationData']

    for variant_dict in gather.data_iterator():

        additional_data_dict={'submission_time': str(datetime.datetime.utcnow())}

        mongo_submission = merge_dicts(variant_dict, additional_data_dict)

        unique_data = get_entries_from_dict(mongo_submission, keys=['chromosome',
                                                                    'start',
                                                                    'ref',
                                                                    'alt',
                                                                    'dataset_name',
                                                                    'data_subset_name',
                                                                    'evidence_type'],
                                            return_type=dict)

        collection.update(unique_data, mongo_submission, upsert=True)




if __name__ == "__main__":
    main()