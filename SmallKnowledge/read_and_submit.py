import csv
import datetime
import argparse
import pymongo
import vcf
from pymongo import MongoClient

script_description="""A protype script for submitting data to MongoDB"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-i','--input', help='Output file name',type=str,metavar='<input_file>', required=True)

args = parser.parse_args()

file = open(args.input)
reader = csv.DictReader(file,delimiter='\t')

client = MongoClient('localhost', 27017)

db = client['SomaticMutations']
collection = db['ValidationData']

def merge_dicts(dict1, dict2):
	new_dict = {}
	for key in dict1: new_dict[key] = dict1[key]
	for key in dict2: new_dict[key] = dict2[key]
	return new_dict

def clean_up_lists(D):
	for key in D:
		if isntance(D[key]) == list: D[key] = D[key][0]
	return D

def stringify_dict(D):
	for key in D:
		if type(D[key]) == list:
			D[key] = map(str,D[key])
		else:
			D[key] = str(D[key])
	return D

for row in reader:
    print row

    tumor_bam = row['tumor_bam']
    normal_bam = row['normal_bam']
    dataset = row['dataset_name']
    evidence_type = row['TP']

    variant_file = open(row['filename'],'r')

    if row['filename'].endswith('.vcf'): variant_file = vcf.Reader(variant_file)

    for record in variant_file:

        print record.INFO
        #print type(record.INFO['alt'])

	if row['filename'].endswith('.vcf'):
	   chrom = record.CHROM
           start = record.POS
           ref = record.REF
           alt = record.ALT

	else:
            if record.startswith('#'): continue

       	    record = record.split('\t')

            chrom = record[0]
            start = record[1]
            ref   = record[3]
            alt   = record[4]

        mongo_data = {"chromosome":chrom,"start":start,"ref":ref,"alt":alt, "tumor_bam":tumor_bam, "normal_bam": normal_bam, "dataset": dataset, "evidence_type": evidence_type,"submission_time": str(datetime.datetime.utcnow())}

        if row['filename'].endswith('.vcf'):
		mongo_data = merge_dicts(mongo_data, record.INFO)

	mongo_data = stringify_dict(mongo_data)

        collection.insert(mongo_data)
