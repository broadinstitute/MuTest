import glob
import os
import csv

def change_extension(filename,extension):
    filestem = os.path.splitext(filename)[0]
    if not extension.startswith("."): extension="."+extension
    return filestem+extension

def get_sample_name(filename):
    sample_name = filename.split('/')
    position = sample_name.index('picard_aggregation')
    return sample_name[position+2]

os.chdir("../data/tcga")

filenames = glob.glob("*database_upload.txt")

def selection_copy(source_file_name, destination_file_name,column,values):

    infile = open(source_file_name,'r')
    reader = csv.DictReader(infile,delimiter='\t')

    outfile = open(destination_file_name,'w')

    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames,delimiter='\t')
    writer.writeheader()

    values = set(values)

    for row in reader:

        if row[column] in values:
            writer.writerow(row)

    infile.close()
    outfile.close()


fieldnames = ['tumor_bam','normal_bam','data_filename','dataset_name','data_subset_name','evidence_type','originator']



outfile = open('../tcga.submission.tsv','w')
writer = csv.DictWriter(outfile, delimiter='\t', fieldnames=fieldnames)
writer.writeheader()

for filename in filenames:

    tumor_type = filename.split('.')[0].lower()
    if not os.path.exists(tumor_type): os.mkdir(tumor_type)

    infile = open(filename)
    reader = csv.DictReader(infile, delimiter='\t')

    for row in reader:

        if row['maf_file_capture_validated_consensus']=='': continue
        if row['tumor_bam']=='': continue
        if row['normal_bam']=='': continue

        sample_id = get_sample_name(row['tumor_bam'])

        maf_filename = ".".join([tumor_type,sample_id,"snp.maf"])

        print "converting ... %s" % sample_id

        out_row={}
        out_row['tumor_bam']  = row['tumor_bam']
        out_row['normal_bam'] = row['normal_bam']
        out_row['data_filename'] = os.path.abspath(os.path.join(tumor_type,maf_filename))
        out_row['dataset_name'] = tumor_type
        out_row['data_subset_name'] = sample_id
        out_row['evidence_type'] = 'TP'
        out_row['originator'] = 'Mara Rosenberg'



        destination = os.path.join(tumor_type,maf_filename)

	tp_destination = change_extension(destination,".tp.maf")
	fp_destination = change_extension(destination,".fp.maf")


        print tp_destination, fp_destination
        continue

        if not os.path.exists(destination):

            selection_copy(source_file_name=row['maf_file_capture_validated_consensus'],
                           destination_file_name=tp_destination,
                           column='validation_status_consensus',
                           values=['TP'])

            selection_copy(source_file_name=row['maf_file_capture_validated_consensus'],
                           destination_file_name=tp_destination,
                           column='validation_status_consensus',
                           values=['FP'])

        writer.writerow(out_row)

