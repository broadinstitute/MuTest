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
    sample_status = int(sample_status[1])
    return bool(sample_status)

def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    return sample_name


samples_index = {}

for row in reader:
    current = row['clean_bam_file_capture']

    sample_name = get_sample_name(current)

    if current != '':
        if is_normal(current):
            samples_index[(sample_name,'tumor')]=current
        else:
            samples_index[(sample_name,'normal')]=current

for sample in samples_index:
    print sample

exit(0)


file = open('/xchip/cga_home/mara/projects/m2/luad/luad.mutation_comparison.master_file.corrected.txt','r')
reader = csv.DictReader(file, delimiter='\t')

fieldnames = move_to_front(['Chromosome','Start_position','Reference_Allele','Tumor_Seq_Allele1','Tumor_Seq_Allele2'],reader.fieldnames)

writer = csv.DictWriter( open('luad.mutation_comparison.master_file.corrected.vcf_column_shuffled.txt','w'), fieldnames = fieldnames, delimiter='\t')

writer.writeheader()

for row in reader:
    print row
    writer.writerow(row)
    exit(0)

file.close()

