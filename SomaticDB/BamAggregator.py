from collections import defaultdict
import ast
import os
import random

import argparse

from somaticDB.Internals.DataGatherer import query_processor
from somaticDB.MongoUtilities import connect_to_mongo


def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    return sample_name

script_description="""A protype script for figuring out what bams one needs to run one's samples on"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-q','--query',
                    help='The query needed to generate the bam lists',
                    type=str,metavar='<query>',
                    required=True)

parser.add_argument('-n','--normal_bam_list',
                    help='The name of the normal bam list to be created.',
                    type=str,
                    metavar='<normal_bam_list>',
                    required=True)

parser.add_argument('-t','--tumor_bam_list',
                    help='The name of the tumor bam list to be created.',
                    type=str ,
                    metavar='<tumor_bam_list>',
                    required=True)

parser.add_argument('-i','--interval_list',
                    help='The name of the intervals list to be created.',
                    type=str ,
                    metavar='<interval_list>',
                    required=True)

parser.add_argument('-o','--output_folder',
                    help='An output folder for the files created.',
                    type=str,
                    metavar='<output_folder>',
                    required=True)



args = parser.parse_args()

collection = connect_to_mongo()

tumor_bam_list  = set([])
normal_bam_list = set([])
interval_list   = defaultdict(set)

query = query = query_processor(args.query)

for record in collection.find(ast.literal_eval(query)):

    if not record.has_key('tumor_bam'):
        print record
        continue

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


