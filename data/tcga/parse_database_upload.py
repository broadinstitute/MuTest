import glob
import os
import csv

filenames = glob.glob("*database_upload.txt")

def selection_copy(source_file_name, destination_file_name,column,values):

    infile = open(source_file_name,'r')
    reader = csv.DictReader(infile,delimiter='\t')


    outfile = open(destination_file_name,'w')
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames,delimiter='\t')

    values = set(values)

    for row in reader:

        if row[column] in values:
            writer.writerow(row)

    infile.close()
    outfile.close()

['indel_maf_file_capture_validated_consensus', 'tumor_bam', 'normal_bam', 'individual_id', 'maf_file_capture_validated_consensus']

outfile = open('tcga.tsv','w')
writer = csv.DictWriter(outfile, delimiter='\t', fieldnames=fieldnames)

for filename in filenames:
    tumor_type = filename.split('.')[0].lower()
    if not os.path.exists(tumor_type): os.mkdir(tumor_type)

    infile = open(filename)
    reader = csv.DictReader(infile, delimiter='\t')

    fieldnames = ['tumor_bam','normal_bam','data_filename','dataset_name','data_subset_name','evidence_type','originator']

    for row in reader:

        maf_filename = ".".join([tumor_type,row['individual_id'],"snp.maf"])

        out_row={}
        out_row['tumor_bam']  = row['tumor_bam']
        out_row['normal_bam'] = row['normal_bam']
        out_row['data_filename'] = os.path.join(tumor_type,maf_filename)
        out_row['dataset_name'] = tumor_type
        out_row['data_subset_name'] = row['individual_id']
        out_row['evidence_type'] = 'TP'
        out_row['originator'] = 'Mara Rosenberg'

        selection_copy(source_file_name=row['maf_file_capture_validated_consensus'],
                       destination_file_name=os.path.join(tumor_type,maf_filename),
                       column='validation_status_consensus',
                       values=['TP'])

        #row['indel_maf_file_capture_validated_consensus'],



        writer.writerow(out_row)

