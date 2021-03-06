import glob
import os
import csv
import hashlib

def change_extension(filename , extension):
    filestem = os.path.splitext(filename)[0]
    if not extension.startswith("."): extension = "." + extension
    return filestem + extension


def get_sample_name(filename):
    sample_name = filename.split('/')
    position = sample_name.index('picard_aggregation')
    return sample_name[position + 2]



def is_same_file_md5(filename1 , filename2):
    code1 = hashlib.md5(open(filename1).read()).hexdigest()
    code2 = hashlib.md5(open(filename2).read()).hexdigest()

    return code1 == code2

def selection_copy(source_file_name , destination_file_name , column , values):
    infile = open(source_file_name , 'r')
    reader = csv.DictReader(infile , delimiter='\t')

    outfile = open(destination_file_name , 'w')

    writer = csv.DictWriter(outfile , fieldnames=reader.fieldnames ,
                            delimiter='\t')
    writer.writeheader()

    values = set(values)

    for row in reader:

        if row[column] in values:
            writer.writerow(row)

    infile.close()
    outfile.close()

def main():

    tcga_dir = "/dsde/working/somaticDB/master/data/tcga"

    if not os.path.exists(tcga_dir): os.mkdir(tcga_dir)

    os.chdir(tcga_dir)

    filenames = glob.glob("*database_upload.txt")


    fieldnames = ['tumor_bam' , 'normal_bam' , 'data_filename' , 'project' ,
                  'dataset','sample', 'evidence_type' , 'author']

    outfile = open('/dsde/working/somaticDB/master/records/tcga.tsv' , 'w')
    writer = csv.DictWriter(outfile , delimiter='\t' , fieldnames=fieldnames)
    writer.writeheader()

    for filename in filenames:

        tumor_type = filename.split('.')[0].lower()
        if not os.path.exists(tumor_type): os.mkdir(tumor_type)

        infile = open(filename)
        reader = csv.DictReader(infile , delimiter='\t')

        for row in reader:

            if row['maf_file_capture_validated_consensus'] == '': continue
            if row['tumor_bam'] == '': continue
            if row['normal_bam'] == '': continue

            sample_id = get_sample_name(row['tumor_bam'])

            maf_filename = ".".join([tumor_type , sample_id , "snp.maf"])

            print "converting ... %s" % sample_id

            out_row = {}
            out_row['tumor_bam'] = row['tumor_bam']
            out_row['normal_bam'] = row['normal_bam']
            out_row['data_filename'] = os.path.abspath(
                os.path.join(tumor_type , maf_filename))
            out_row['project'] = 'tcga'
            out_row['dataset'] = tumor_type
            out_row['sample'] = sample_id
            out_row['evidence_type'] = 'TP'
            out_row['author'] = 'Mara Rosenberg'

            destination = os.path.join(tumor_type , maf_filename)

            tp_destination = os.path.abspath(change_extension(destination , ".tp.maf"))
            fp_destination = os.path.abspath(change_extension(destination , ".fp.maf"))

            if not os.path.exists(tp_destination):
                selection_copy(
                    source_file_name=row['maf_file_capture_validated_consensus'] ,
                    destination_file_name=tp_destination ,
                    column='validation_status_consensus' ,
                    values=['TP' , 'TP_HighConf'])

            if not os.path.exists(fp_destination):
                selection_copy(
                    source_file_name=row['maf_file_capture_validated_consensus'] ,
                    destination_file_name=fp_destination ,
                    column='validation_status_consensus' ,
                    values=['FP'])

            out_row['data_filename'] = tp_destination
            out_row['evidence_type'] = 'TP'
            writer.writerow(out_row)
            out_row['data_filename'] = fp_destination
            out_row['evidence_type'] = 'FP'
            writer.writerow(out_row)

if __name__ == '__main__':
    main()