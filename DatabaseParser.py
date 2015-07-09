import gzip
from itertools import ifilter
import csv

import vcf

from somaticDB.DictUtilities import merge_dicts , stringify_dict


def adjustIndelFormat(start_position, ref, alt):
    end_position = start_position
    if len(alt) > 1:
        #insertion
        if not alt.startswith("<"): alt = alt[1:]
        ref = "-"
        end_position = start_position + 1

    elif len(ref) > 1:
        #deletion
        alt = "-"
        if not ref.startswith("<"): ref = ref[1:]
        start_position += 1
        end_position = start_position + len(ref) - 1
    else:
        end_position = start_position
    return start_position, end_position, ref, alt


class DatabaseParser:
    """
        The DatabaseParser collects information and stores it.
    """
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
            if any([self.filename.endswith(".table"),
                   self.filename.endswith(".table.gz")]):
                dataset_type = "VCF_TABLE"

            if any([self.filename.endswith(".vcf"),
                   self.filename.endswith(".vcf.gz")]):
                dataset_type = "VCF"

            if any([self.filename.endswith(".maf"),
                   self.filename.endswith(".maf.gz")]):
                dataset_type = "MAF"

        if dataset_type not in ['VCF', 'MAF', 'VCF_TABLE']:
            raise Exception("Bad file format: %s"%self.filename)

        if dataset_type == 'VCF':
            self.file = vcf.Reader(self.file)
        else:
            self.file = ifilter(lambda line: not line.startswith('#'), self.file)
            self.file = csv.DictReader(self.file,delimiter='\t')

        for record in self.file:
            if dataset_type == 'VCF':
                for k, alt in enumerate(record.ALT): #split biallelic sites
                    chrom = record.CHROM
                    start = record.POS
                    ref = record.REF
                    alt = str(alt)

                    filter = record.FILTER

                    start, end, ref, alt = adjustIndelFormat(start, ref, alt)

                    core_data = {"chromosome":chrom,"start":start,"end":end,"ref":ref,"alt":alt,"FILTER":filter}

                    for key in record.INFO:
                        if key in ['MLEAC','MLEAF','AC','AF']:
                            core_data[key] = record.INFO[key][k]
                        else:
                            core_data[key] = record.INFO[key]


                    core_data = merge_dicts(core_data,record.INFO)

                    core_data = stringify_dict(core_data)

                    yield core_data


            if dataset_type == 'VCF_TABLE':
                ALT = record['ALT'].split(",")

                for k, alt in enumerate(ALT):
                    chrom = record['CHROM']
                    start = record['POS']
                    ref = record['REF']

                    start, end, ref, alt = adjustIndelFormat(start, ref, alt)

                    core_data = {"chromosome":chrom,"start":start,"end":end,"ref":ref,"alt":alt}

                    mleac = record['MLEAC'].split(',')
                    mleaf = record['MLEAF'].split(',')
                    ac = record['AC'].split(',')
                    af = record['AF'].split(',')

                    for key in record:

                        if key in ['CHROM','POS','REF','MLEAF','MLEAC','AC','AF']: continue

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
                                core_data[key] = core_data[key].split(',')[k]

                    core_data = stringify_dict(core_data)

                    yield core_data

            if dataset_type == "MAF":

                chrom = record['Chromosome']
                start = record['Start_position']
                end = record['End_position']
                ref   = record['Reference_Allele']
                alt   = record['Tumor_Seq_Allele2']

                core_data = {"chromosome":chrom,"start":start,"end":end,"ref":ref,"alt":alt}

                for key in record:
                    if key not in ['Chromosome','Start_Position','End_Position','Reference_Allele','Tumor_Seq_Allele1','Tumor_Seq_Allele2']:
                        core_data[key] = record[key]

                core_data = stringify_dict(core_data)

                yield core_data
