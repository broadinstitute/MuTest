
import csv
import argparse
import datetime
from pymongo import MongoClient
from DictUtilities import merge_dicts
from somaticDB import DatabaseParser
from somaticDB.DictUtilities import get_entries_from_dict


class DataGatherer:
    def __init__(self, filename):
        self.filename = filename

    def data_iterator(self):
        file = open(self.filename)
        reader = csv.DictReader(file,delimiter='\t')

        for file_data in reader:

            meta_data_dict = get_entries_from_dict(file_data,

                                                   keys=['tumor_bam',
                                                         'normal_bam',
                                                         'dataset_name',
                                                         'data_subset_name',
                                                         'TP'],

                                                   return_type=dict)

            D = DatabaseParser(meta_data_dict['data_filename'])

            for variant_dict in D.get_variants():

                yield merge_dicts(variant_dict, meta_data_dict)


def adjustIndelFormat(start_position, ref, alt):
    end_position = start_position
    if len(alt) > 1:
        #insertion
        alt = alt[1:]
        ref = "-"
        end_position = start_position + 1

    elif len(ref) > 1:
        #deletion
        alt = "-"
        ref = ref[1:]
        start_position += 1
        end_position = start_position + len(ref) - 1
    else:
        raise Exception('Should not be here')
    return start_position, end_position, ref, alt



def main():
    script_description="""A protype script for submitting data to MongoDB"""
    script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                    description=script_description,
                                    epilog=script_epilog,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('-i','--input', help='Input file name',type=str,metavar='<input_file>', default="ALL",required=True)
    parser.add_argument('-p','--port', help='Input file name',type=int,metavar='<input_file>', default=27017,required=True)

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
                                                                    'TP'],
                                            type=dict)

        collection.update(unique_data, mongo_submission, upsert=True)




if __name__ == "__main__":
    main()