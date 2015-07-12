import os
import csv
import glob


def change_extension(filename,extension):
    filestem = os.path.splitext(filename)[0]
    if not extension.startswith("."): extension="."+extension
    return filestem+extension


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

def main():
    location = os.getcwd()

    for directory in ['hcc1143','hcc1954']:
        os.chdir(location)

        print os.getcwd()

        filenames = glob.glob('/dsde/working/somaticDB/master/originals/%s/*.maf'%directory)

        for filename in filenames:

            destination = os.path.basename(filename)

            destination = os.path.join('/dsde/working/somaticDB/master/data/%s/%s//'%(directory,directory),destination)


            tp_destination = change_extension(destination,".tp.maf")
            fp_destination = change_extension(destination,".fp.maf")



            selection_copy(source_file_name=filename,
                               destination_file_name=tp_destination,
                               column='Status',
                               values=['TP'])


            selection_copy(source_file_name=filename,
                               destination_file_name=fp_destination,
                               column='Status',
                               values=['FP','UNKNOWN'])

if __name__ == '__main__':
    main()