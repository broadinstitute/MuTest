import argparse
import pymongo
import ast
from pymongo import MongoClient

def pp_dict(x):
	for key in x.keys():
		print key+": "+str(x[key])


script_description="""A protype script that accesses true and false positives"""
script_epilog="""Created for evaluation of performance of Mutect 2 """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i','--input', help='The file to be assessed',type=str,metavar='<input_file>', required=True)
parser.add_argument('-q','--query', help='The query for the dataset needed',type=str,metavar='<query>', required=True)
parser.add_argument('-D','--demo', help='Print information as part of a demo',action='store_true', default=False)

args = parser.parse_args()

client = MongoClient('localhost', 27017)
db = client['SomaticMutations']
collection = db['ValidationData']

algorithm_data = set([])

file = open(args.input)
for record in file:
	if record.startswith('#'): continue
	record = record.split('\t')

	chrom = record[0]
	start = record[1]
	ref = record[3]
	alt = record[4]

	algorithm_data.add( (chrom,start,ref,alt) )

for thing in sorted( list(algorithm_data), key=lambda s: s[1]):
	0#print "former:", thing


TP = 0; P = 0; FP = 0; N = 0;

data_collection=[]

for record in collection.find(ast.literal_eval(args.query)):
	if args.demo:
		pp_dict(record)
		print 

	confirmation_data = tuple([record[key] for key in ['chromosome','start','ref','alt']])

	confirmation_data = tuple(map(str, confirmation_data))

	evidence_type = record['evidence_type']

	if evidence_type == 'TP':
		P+=1
		if confirmation_data in algorithm_data: TP+=1

	if evidence_type == 'FP':
		N+=1
		if confirmation_data in	algorithm_data: FP+=1

	data_collection.append(confirmation_data)

for thing in sorted(data_collection,key=lambda x: x[1]):
	print thing

print "True positives:  ", TP
print "Known positives: ", P
print "False positives: ", FP
print "Known negatives: ", N
