import csv

from somaticDB import DatabaseParser

from somaticDB.DictUtilities import merge_dicts , tally
from somaticDB.DictUtilities import get_entries_from_dict


def query_processor(selections):
    if selections.startswith('{'):
        query = selections
    elif selections == 'all':
        query = '{project : { $exists : true } }'
    else:
        selections = selections.split(',')
        selections = [selection.split(':') for selection in selections]

        print selections

        selections = tally(selections)

        query='$or{'

        midquery = list()
        for selection in selections:
            midquery.append('{'+selection+':'+str(selections[selection])+'}')

        query += ','.join(midquery)

        query+='}'

    return query




class DataGatherer:
    def __init__(self, filename):
        self.filename = filename
        self.new_file = False

    def data_iterator(self, demo=False,keys=('tumor_bam',
                                             'normal_bam',
                                             'data_filename',
                                             'dataset_name',
                                             'data_subset_name',
                                             'evidence_type')):
        file = open(self.filename,'rU')
        reader = csv.DictReader(file,delimiter='\t')

        for file_data in reader:

            meta_data_dict = get_entries_from_dict(file_data,
                                                   keys=keys,
                                                   return_type=dict)

            D = DatabaseParser(meta_data_dict['data_filename'])

            n=0

            self.new_file = True

            for variant_dict in D.get_variants():
                n+=1
                if demo:
                    if (n > 50): break
                yield merge_dicts(variant_dict, meta_data_dict)
                if self.new_file == True: self.new_file = False