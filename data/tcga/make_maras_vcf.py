import csv
import os
import pandas as pd

filename = "/xchip/cga_home/mara/projects/m2/luad/fh.m2_evaluation_set.bam_file_paths.txt"

def move_to_front(selections, columns):
    selection_index = []
    for selection in selections: selection_index.append(columns.index(selection))
    selection_set = set(selection_index)
    remainder = [k for k in range(len(columns)) if k not in selection_set]
    remainder = selection_index+remainder
    return [columns[k] for k in remainder]


file = open(filename,'r')
reader = csv.DictReader(file,delimiter='\t')

def is_normal(sample_path):
    sample_name = os.path.basename(sample_path)
    sample_status = sample_name.split('-')[3]
    sample_status = int(sample_status[0])
    return bool(sample_status)

def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    sample_name = sample_name.split('-')[0:3]
    sample_name = "-".join(sample_name)
    return sample_name


samples_index = {}

for row in reader:
    current = row['clean_bam_file_capture']

    sample_name = get_sample_name(current)

    if current != '':
        if is_normal(current):
            if samples_index.has_key((sample_name,'tumor')): raise Exception("Sample ID duplicated in file."+sample_name)
            samples_index[(sample_name,'tumor')]=current
        else:
            if samples_index.has_key((sample_name,'normal')): raise Exception("Sample ID duplicated in file."+sample_name)
            samples_index[(sample_name,'normal')]=current


file = open('/xchip/cga_home/mara/projects/m2/luad/luad.mutation_comparison.master_file.corrected.txt','r')
reader = csv.DictReader(file, delimiter='\t')

writer = {}

for row in reader:
    sample_name = row['Tumor_Sample_Barcode'].split('-')[1:4]
    sample_name = "-".join(sample_name)

    print sample_name

    if ((sample_name,'tumor') in samples_index) | ((sample_name,'normal') in samples_index):
        pass
    else:
        print sample_name
    for key in sorted(row.keys()):


file.close()

