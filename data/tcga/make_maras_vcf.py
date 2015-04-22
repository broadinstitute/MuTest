import csv
import os

filename = "luad/fh.m2_evaluation_set.bam_file_paths.txt"

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


filename = 'luad/luad.mutation_comparison.master_file.corrected.tsv'
file = open(filename,'r')
file_stem = os.path.splitext( filename)[0]
file_ext=".maf"
reader = csv.DictReader(file, delimiter='\t')

submission_filename = "luad.submit.txt"

submission_file = open(submission_filename,'w')
submission_file = csv.DictWriter(submission_file,
                                 fieldnames=['tumor_bam','normal_bam','filename','dataset_name','TP'],
                                 delimiter='\t')

submission_file.writeheader()

writer = {}

for row in reader:
    sample_name = row['Tumor_Sample_Barcode'].split('-')[1:4]
    sample_name = "-".join(sample_name)

    if ((sample_name,'tumor') not in samples_index) | ((sample_name,'normal') not in samples_index):
        raise Exception("Missing sample.")

    if not writer.has_key(sample_name):

        sample_filename = file_stem+"."+sample_name+file_ext

        writer[sample_name] = csv.DictWriter(open(sample_filename,'w'),
                                             delimiter='\t',
                                             fieldnames=reader.fieldnames)

        writer[sample_name].writeheader()

        submission_file.writerow({'tumor_bam': samples_index[(sample_name,'tumor')],
                                   'normal_bam': samples_index[(sample_name,'normal')],
                                   'filename':os.path.abspath(sample_filename),
                                   'dataset_name':'LUAD',
                                   'TP':'TP'})

    writer[sample_name].writerow(row)


file.close()

