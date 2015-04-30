import glob
import os
import csv

filenames = glob.glob("*database_upload.txt")

def selection_copy(source_file_names, destination_file_name,column,values):
        infile = open(source_file_name,'r')
        reader = csv.DictReader(infile)
        outfile = open(destination_file_name,'w')
        writer = csv.WriterReader(outfile, fieldnames=reader.fieldnames)

        values = set(values)

        for row in reader:
                if row[column] in values:
                        writer.writerow(row)

        infile.close()
        outfile.close()

for filename in filenames:
	tumor_type = filename.split('.')[0].lower()
	if not os.path.exists(sample): os.mkdir(tumor_type)

	infile = open(filename)
	reader = csv.DictReader(outfile, delimiter='\t')

	fieldnames = ['tumor_bam','normal_bam','data_filename','dataset_name','data_subset_name','evidence_type','originator']



	for row in reader:
		print row	
		print row.keys()

		out_row={}
		out_row['tumor_bam']  = row['tumor_bam']
		out_row['normal_bam'] = row['normal_bam']
		out_row['data_filename'] = 
		out_row['dataset_name'] = tumor_type
		out_row['data_subset_name'] = row[]
		out_row['evidence_type'] = 'TP'
		out_row['originator'] = 'Mara Rosenberg'

		break

	break
