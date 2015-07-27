from collections import defaultdict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.DataGatherer import query_processor
import ast
import csv

def NormalNormalAggregator(normal_bam_list, tumor_bam_list,query, output_filename):

    collection = connect_to_mongo(collection='NormalNormalData')

    query = query_processor(query)

    bam_sets=defaultdict(set)

    for record in collection.find(ast.literal_eval(query)):
        bam_sets[(record['project'],record['dataset'])].add((record['sample'],record['file']))
        print record

    fieldnames=['tumor_bam','normal_bam','data_filename','project','dataset','sample','evidence_type','author']
    file = csv.DictWriter(open(output_filename,'w'), fieldnames=fieldnames,delimiter='\t')


    normal_bam_list = open(normal_bam_list,'w')
    tumor_bam_list  = open(tumor_bam_list,'w')

    for bam_set in bam_sets:

        bams = list(bam_sets[bam_set])
        n = len(bams)

        project = bam_set[0]
        dataset = bam_set[1]

        for i in range(n):
            for j in range(n):
                if i == j: continue

                sample1,bam1 = bams[i]
                sample2,bam2 = bams[j]

                row={'tumor_bam':bam1,
                 'normal_bam':bam2,
                 'data_filename':'.' ,
                 'project': project,
                 'dataset': dataset,
                 'sample': '%s-%s'%(sample1,sample2),
                 'evidence_type': 'NN',
                 'author': 'None'}

                normal_bam_list.write(bam1+'\n')
                tumor_bam_list.write(bam2+'\n')

                file.writerow(row)
