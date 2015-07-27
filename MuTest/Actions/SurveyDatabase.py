import ast
from collections import defaultdict
import csv
import logging
from MuTest.BasicUtilities.DictUtilities import get_entries_from_dict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo


def survey(filename):

    logging.getLogger(__name__).info("Beginning survey.")

    query = "{'project' : { '$exists' : 'true' } }"

    tally = defaultdict(int)

    collector = connect_to_mongo()

    # collect query information
    n = 0
    for record in collector.find(ast.literal_eval(query)):

        sample_information = get_entries_from_dict(record, keys=['project',
                                                                 'dataset',
                                                                 'sample',
                                                                 'evidence_type'],return_type=dict)


        if sample_information['evidence_type'] == 'TP':
            n+=1
            project = sample_information['project']
            dataset = sample_information['dataset']
            sample  = sample_information['sample']

            tally[(project,dataset,sample)]+=1
            tally[(project,dataset,'')]+=1
            tally[(project,'','')]+=1
            tally[('all','all','all')]+=1

            if not (n % 10000): logging.getLogger(__name__).info("Variants seen: "+str(n))


    fp = csv.DictWriter(open(filename,'w'), fieldnames=['project','dataset','sample','count'],delimiter='\t')

    for item in tally:
        fp.writerow({'project':item[0],'dataset':item[1],'sample':item[2],'count': tally[item] })