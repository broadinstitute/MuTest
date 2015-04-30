import glob
import os
import csv

filenames = glob.glob("*database_upload.txt")

def selection_copy(source_file_names, destination_file_name,column,values):

    outfile = None

    for source_file_name in source_file_names:
        infile = open(source_file_name,'r')
        reader = csv.DictReader(infile)

        if outfile is not None:
            outfile = open(destination_file_name,'w')
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames,delimiter='\t')

        values = set(values)

        for row in reader:

            print row.keys()

            if row[column] in values:
                writer.writerow(row)

        infile.close()
    outfile.close()

['indel_maf_file_capture_validated_consensus', 'tumor_bam', 'normal_bam', 'individual_id', 'maf_file_capture_validated_consensus']


for filename in filenames:
    tumor_type = filename.split('.')[0].lower()
    if not os.path.exists(tumor_type): os.mkdir(tumor_type)

    infile = open(filename)
    reader = csv.DictReader(infile, delimiter='\t')

    fieldnames = ['tumor_bam','normal_bam','data_filename','dataset_name','data_subset_name','evidence_type','originator']

    outfile = open('tcga.tsv','w')
    writer = csv.DictWriter(outfile, delimiter='\t', fieldnames=fieldnames)

    for row in reader:

        maf_filename = ".".join([tumor_type,row['individual_id'],"maf"])

        out_row={}
        out_row['tumor_bam']  = row['tumor_bam']
        out_row['normal_bam'] = row['normal_bam']
        out_row['data_filename'] = os.path.join(tumor_type,maf_filename)
        out_row['dataset_name'] = tumor_type
        out_row['data_subset_name'] = row['individual_id']
        out_row['evidence_type'] = 'TP'
        out_row['originator'] = 'Mara Rosenberg'

        selection_copy(source_file_names=[row['indel_maf_file_capture_validated_consensus'],
                                          row['maf_file_capture_validated_consensus']],
                       destination_file_name=maf_filename,
                       column='validation_status_consensus',
                       values=['TP'])

        writer.writerrow(out_row)

        break

    break
