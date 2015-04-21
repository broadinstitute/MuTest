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


filename = '/xchip/cga_home/mara/projects/m2/luad/luad.mutation_comparison.master_file.corrected.txt'
file = open(filename,'r')
reader = csv.DictReader(file, delimiter='\t')


#writer = csv.DictWriter( open('luad.mutation_comparison.master_file.corrected.vcf_column_shuffled.txt','w'),fieldnames = reader.fieldnames,delimiter='\t')
#writer.writeheader()

outfile = {}

file_stem,file_ext = os.path.splitext( os.path.basename(filename) )

for row in reader:
    sample_name = row['Tumor_Sample_Barcode'].split('-')[1:4]
    sample_name = "-".join(sample_name)

    if not outfile.has_key(sample_name):
        outfile[sample_name] = open(file_stem+"."+sample_name+file_ext,'w')
        outfile[sample_name] = csv.DictWriter(outfile,fieldnames = reader.fieldnames,delimiter='\t')

    if ((sample_name,'tumor') in samples_index) | ((sample_name,'normal') in samples_index):
	pass
    else:
        raise Expection("A sample ID is not unique: %s" % sample_name)

    outfile.writerow(row)
    #exit(0)

file.close()

