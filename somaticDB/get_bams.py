from collections import defaultdict
import argparse
import ast
import os
from pymongo import MongoClient
import random

def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    sample_name = sample_name.split('-')[0:3]
    sample_name = "-".join(sample_name)
    return sample_name

script_description="""A protype script for figuring out what bams one needs to run one's samples on"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-q','--query', help='The query needed to generate the bam list',type=str,metavar='<query>', required=True)

parser.add_argument('-n','--normal_bam_list',
                    help='normal bam list',
                    type=str,
                    metavar='<normal_bam_list>',
                    required=True)

parser.add_argument('-t','--tumor_bam_list',
                    help='tumor bam list',
                    type=str ,
                    metavar='<tumor_bam_list>',
                    required=True)

parser.add_argument('-i','--interval_list',
                    help='interval list',
                    type=str ,
                    metavar='<interval_list>',
                    required=True)

parser.add_argument('-p','--port', help='Port.',type=int,metavar='<port>', default=27017)

args = parser.parse_args()

client = MongoClient('localhost', args.port)
db = client['SomaticMutations']
collection = db['ValidationData']

tumor_bam_list  = set([])
normal_bam_list = set([])
interval_list   = defaultdict(set)

for record in collection.find(ast.literal_eval(args.query)):
    tumor_bam  = record['tumor_bam']
    normal_bam = record['normal_bam']

    interval = "%s:%s-%s" % (record['chromosome'],
                             record['start'],
                             record['end'])

    interval_list[(tumor_bam, normal_bam)].add(interval)

tumor_bam_file = open(args.tumor_bam_list,'w')
normal_bam_file = open(args.normal_bam_list,'w')
interval_file = open(args.interval_list,'w')

file_stem, file_ext = os.path.splitext(args.tumor_bam_list)

for pair in interval_list:
    tumor_bam, normal_bam = pair
    tumor_bam_file.write(tumor_bam+'\n')
    normal_bam_file.write(normal_bam+'\n')

    #sample = get_sample_name(tumor_bam)
    sample =\
        "".join([random.choice('abcdef0123456789') for k in range(40)])

    print sample

    current_filename = "intervals."+sample+".list"

    current_interval_file = open(current_filename,'w')

    for interval in list(interval_list[pair]):
        current_interval_file.write(interval+"\n")

    current_interval_file.close()

    interval_file.write( current_filename +'\n')

tumor_bam_file.close()
normal_bam_file.close()
interval_file.close()


