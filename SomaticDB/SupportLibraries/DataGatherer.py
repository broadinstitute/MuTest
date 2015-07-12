import csv

from SomaticDB.BasicUtilities.DictUtilities import get_entries_from_dict , merge_dicts , \
    tally
from SomaticDB.SupportLibraries.DatabaseParser import DatabaseParser


def query_processor(selections):
    if selections.startswith('{'):
        query = selections
    elif selections == 'all':
        query = "{'project' : { '$exists' : 'true' } }"
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
        self.current_file = None

    def data_iterator(self,keys=('tumor_bam','normal_bam',
                                             'data_filename',
                                             'project',
                                             'dataset',
                                             'evidence_type')):
        file = open(self.filename,'rU')
        reader = csv.DictReader(file,delimiter='\t')

        for file_data in reader:

            if file_data.has_key('FILTER'):
                if len(filter) > 0: continue

            meta_data_dict = get_entries_from_dict(file_data,
                                                   keys=keys,
                                                   return_type=dict)

            D = DatabaseParser(meta_data_dict['data_filename'])
            self.current_file = meta_data_dict['data_filename']

            n=0

            self.new_file = True

            for variant_dict in D.get_variants():
                yield merge_dicts(variant_dict, meta_data_dict)
                if self.new_file == True: self.new_file = False

        self.current_file = None