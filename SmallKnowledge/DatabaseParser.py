
import gzip
import vcf
import csv
import argparse
import datetime
from pymongo import MongoClient
from DictUtilities import merge_dicts, stringify_dict

class DatabaseParser:

    def __init__(self,filename):
        self.filename = filename
        self.refresh()

    def refresh(self):
        if self.filename.endswith(".gz"):
            self.file = gzip.open(self.filename, 'r')
        else:
            self.file = open(self.filename, 'r')

    def get_variants(self, dataset_type=None):

        if dataset_type is None:
            if any(self.filename.endswith(".table"),
                   self.filename.endswith(".table.gz")):
                dataset_type = "VCF_TABLE"

            if any(self.filename.endswith(".vcf"),
                   self.filename.endswith(".vcf.gz")):
                dataset_type = "VCF"

            if any(self.filename.endswith(".maf"),
                   self.filename.endswith(".maf.gz")):
                dataset_type = "MAF"

        if dataset_type not in ['VCF', 'MAF', 'VCF_TABLE']:
            raise Exception("Bad file format: %s"%self.filename)

        if dataset_type == 'VCF':
            self.file = vcf.Reader(self.file)
        else:
            self.file = csv.DictReader(self.file)

        for record in self.file:
            if dataset_type == 'VCF':
                for k, alt in enumerate(record.ALT): #split biallelic sites
                    chrom = record.CHROM
                    start = record.POS
                    ref = record.REF
                    alt = str(alt)

                    core_data = {"chromosome":chrom,"start":start,"ref":ref,"alt":alt}

                    for key in record.INFO:
                        if key in ['MLEAC','MLEAF','AC','AF']:
                            core_data[key] = record.INFO[key][k]
                        else:
                            core_data[key] = record.INFO[key]


            if dataset_type == 'VCF_TABLE':
                ALT = record['ALT'].split(",")

                for k, alt in enumerate(ALT):
                    chrom = record['CHROM']
                    start = record['POS']
                    ref = record['REF']

                core_data = {"chromosome":chrom,"start":start,"ref":ref,"alt":alt}

                mleac = record['MLEAC'].split(',')
                mleaf = record['MLEAF'].split(',')
                ac = record['AC'].split(',')
                af = record['AF'].split(',')

                for key in record:
                        if key == 'MLEAC':
                            core_data['MLEAC'] = mleac[k]
                        elif key == 'MLEAF':
                            core_data['MLEAF'] = mleaf[k]
                        elif key == 'AC':
                            core_data['AC'] = ac[k]
                        elif key == 'AF':
                            core_data['AF'] = af[k]
                        else:
                            core_data[key] = record[key]

                            if "," in core_data[key]:
                                core_data[key] = core_data[key].split(',')

            if dataset_type == "MAF":







def main():
    script_description="""A protype script for submitting data to MongoDB"""
    script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                    description=script_description,
                                    epilog=script_epilog,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('-i','--input', help='Input file name',type=str,metavar='<input_file>', required=True)

    args = parser.parse_args()

    file = open(args.input)
    reader = csv.DictReader(file,delimiter='\t')

    client = MongoClient('localhost', 27017)
    db = client['SomaticMutations']
    collection = db['ValidationData']

    for file_data in reader:
        tumor_bam     = file_data['tumor_bam']
        normal_bam    = file_data['normal_bam']
        dataset       = file_data['dataset_name']
        evidence_type = file_data['TP']

        D = DatabaseParser(file_data['filename'])

        for variant_dict in D.get_variants():


            additional_data_dict={'tumor_bam'      : tumor_bam,
                                  'normal_bam'     : normal_bam,
                                  'dataset'        : dataset,
                                  'evidence_type'  : evidence_type,
                                  'submission_time': str(datetime.datetime.utcnow())}

            mongo_submission = merge_dicts(variant_dict, additional_data_dict)

            collection.insert(mongo_submission)



if __name__ == "__main__":
    main()