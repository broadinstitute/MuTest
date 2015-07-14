import argparse
from SomaticDB.Actions import VariantUploader
from SomaticDB.Actions.BamAggregator import BamAggregator
from SomaticDB.Actions.VariantAssessor import VariantAssessor


def main():

    description = '\nSomatic Caller Assessor'

    epilog = """Created as a testing framework for somatic mutation callers.\n\n"""

    parser = argparse.ArgumentParser(description=description,
                     epilog=epilog,
                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(help='commands',dest='subparser')

    bam_aggregator_parser = subparsers.add_parser('bam_aggregator',
                         help  ='Produces a list of bams for an assessment.')


    bam_aggregator_parser.add_argument('-q','--query',
                        help='The query needed to generate the bam lists',
                        type=str,metavar='<query>',
                        required=True)

    bam_aggregator_parser.add_argument('-n','--normal_bam_list',
                        help='The name of the normal bam list to be created.',
                        type=str,
                        metavar='<normal_bam_list>',
                        required=True)

    bam_aggregator_parser.add_argument('-t','--tumor_bam_list',
                        help='The name of the tumor bam list to be created.',
                        type=str ,
                        metavar='<tumor_bam_list>',
                        required=True)

    bam_aggregator_parser.add_argument('-i','--interval_list',
                        help='The name of the intervals list to be created.',
                        type=str ,
                        metavar='<interval_list>',
                        required=True)

    bam_aggregator_parser.add_argument('-o','--output_folder',
                        help='An output folder for the files created.',
                        type=str,
                        metavar='<output_folder>',
                        required=True)


    variant_assessor_parser = subparsers.add_parser('variant_assessor',
                         help  ='Produces a list of bams for an assessment.')


    variant_assessor_parser.add_argument('-t','--tsv', help='The list of datasets to be assessed.',type=str,metavar='<tsv>', required=True)
    variant_assessor_parser.add_argument('-q','--query', help='The query for the dataset needed',type=str,metavar='<query>', required=True)


    variant_uploader_parser = subparsers.add_parser('variant_uploader',
                         help  ='Produces a list of bams for an assessment.')


    variant_uploader_parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)

    args = parser.parse_args()

    if (args.subparser == "bam_aggregator"):
        BamAggregator(args.query, args.normal_bam_list, args.tumor_bam_list, args.interval_list)


    if (args.subparser == "variant_assessor"):
        VariantAssessor(args.query,args.tsv)

    if (args.subparser == "variant_uploader"):
        VariantUploader(args.tsv)
