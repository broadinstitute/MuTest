from collections import defaultdict
import ast
import os
import random
import csv

import argparse
from MuTest.BasicUtilities.DictUtilities import get_entries_from_dict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.DataGatherer import query_processor
from MuTest.SupportLibraries.SomaticFileSystem import SomaticFileSystem

import re

def picard_version_to_current(path):
    return re.sub('/v\d+/','/current/',path)

def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    return sample_name

script_description="""A protype script for figuring out what bams one needs to run one's samples on"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """


def BamAggregator(query, normal_bam_list_name, tumor_bam_list_name, interval_list_name, metadata_list_name, folder):

    collection = connect_to_mongo()



    query = query_processor(query)

    interval_list = defaultdict(set)

    metadata_list = {}


    for record in collection.find(ast.literal_eval(query)):

        if not record.has_key('tumor_bam'):
            print record
            continue

        #print record['tumor_bam']

        record['tumor_bam']=picard_version_to_current(record['tumor_bam'])
        record['normal_bam']=picard_version_to_current(record['normal_bam'])

        #print record['tumor_bam']
        #print

        tumor_bam  = record['tumor_bam']
        normal_bam = record['normal_bam']

        interval = "%s:%s-%s" % (record['chromosome'],
                                 record['start'],
                                 record['end'])

        interval_list[(tumor_bam, normal_bam)].add(interval)

        field_names=['tumor_bam','normal_bam','data_filename','project','dataset','sample']
        metadata_list[(tumor_bam, normal_bam)] = get_entries_from_dict(record,keys=field_names,return_type=dict)
        metadata_list[(tumor_bam, normal_bam)]['evidence_type'] = '.'
        metadata_list[(tumor_bam, normal_bam)]['author']='.'

    tumor_bam_file = open(tumor_bam_list_name,'w')
    normal_bam_file = open(normal_bam_list_name,'w')
    interval_file = open(interval_list_name,'w')

    fieldnames=['tumor_bam','normal_bam','data_filename','project','dataset','sample','evidence_type','author']
    metadata_file = csv.DictWriter(open(metadata_list_name,'w'),fieldnames=fieldnames,delimiter='\t')
    metadata_file.writeheader()

    current_dir = os.getcwd()

    for pair in interval_list:
        tumor_bam, normal_bam = pair
        tumor_bam_file.write(tumor_bam+'\n')
        normal_bam_file.write(normal_bam+'\n')

        metadata_file.writerow(metadata_list[(tumor_bam, normal_bam)])

        sample =\
            "".join([random.choice('abcdef0123456789') for k in range(40)])

        intervals_dir = os.path.join(current_dir, folder)

        current_filename = "intervals."+sample+".list"
        current_filename = os.path.join(intervals_dir, current_filename)

        if not os.path.exists(intervals_dir): os.mkdir(intervals_dir)

        current_interval_file = open(current_filename,'w')

        sorted_intervals = sorted(list(interval_list[pair]),key=lambda x: int(x.split(':')[1].split('-')[0]))

        sorted_intervals = sorted(sorted_intervals,key=lambda x:x.split(':'))


        for interval in sorted_intervals:
            current_interval_file.write(interval+"\n")

        current_interval_file.close()

        interval_file.write( current_filename +'\n')

    tumor_bam_file.close()
    normal_bam_file.close()
    interval_file.close()

