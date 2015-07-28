import ast
from collections import defaultdict
import csv
import logging
from MuTest.BasicUtilities.DictUtilities import get_entries_from_dict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.Variant import is_snp , is_indel


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


        if is_snp(record):
            feature = 'snp'
        if is_indel(record):
            feature = 'indel'


        if sample_information['evidence_type'] == 'TP':
            n+=1
            project = sample_information['project']
            dataset = sample_information['dataset']
            sample  = sample_information['sample']

            tally[(project,dataset,sample,feature)]+=1
            tally[(project,dataset,'',feature)]+=1
            tally[(project,'','',feature)]+=1
            tally[('','','',feature)]+=1

            if not (n % 10000): logging.getLogger(__name__).info("Variants seen: "+str(n))


    fp = csv.DictWriter(open(filename,'w'), fieldnames=['project','dataset','sample','feature','count'],delimiter='\t')

    fp.writeheader()

    for item in tally:
        fp.writerow({'project':item[0],'dataset':item[1],'sample':item[2],'feature':item[3],'count': tally[item] })