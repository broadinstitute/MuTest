import argparse
import pymongo
import ast
from pymongo import MongoClient

script_description="""A protype script for figuring out what bams one needs to run one's samples on"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-q','--query', help='The query needed to generate the bam list',type=str,metavar='<query>', required=True)
parser.add_argument('-o','--output_file',help='The file to output the bam list to',type=str,metavar='<output_file>',required=True)

args = parser.parse_args()

client = MongoClient('localhost', 27017)
db = client['SomaticMutations']
collection = db['ValidationData']

bam_list=set([])

for record in collection.find(ast.literal_eval(args.query)):
	 bam_list.add((record['tumor_bam'],record['normal_bam']))

bam_list =list(bam_list)

outfile = open(args.output_file,'w')
for bam in bam_list:
	print >>outfile,"\t".join(bam)

outfile.close()

