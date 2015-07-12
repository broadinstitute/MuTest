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

    bam_aggregator_parser = subparsers.add_parser('bam_aggregate',
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


    variant_assessor_parser = subparsers.add_parser('variant_assess',
                         help  ='Assesses a file of variants against truth data stored in the mongo database.')


    variant_assessor_parser.add_argument('-t','--tsv', help='The list of datasets to be assessed.',type=str,metavar='<tsv>', required=True)
    variant_assessor_parser.add_argument('-q','--query', help='The query for the dataset needed',type=str,metavar='<query>', required=True)


    variant_uploader_parser = subparsers.add_parser('variant_upload',
                         help  ="Uploads data both to mongo. WARNING: ONLY FOR INTERNAL USE. If you are an external user, please use 'variant_submit' instead")


    variant_uploader_parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)


    variant_submitter_parser = subparsers.add_parser('variant_submit',
                         help  ='Sumbits data both to mongo and stores information on the filesystem (at /dsde)')


    variant_submitter_parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)


    args = parser.parse_args()

    if (args.subparser == "bam_aggregate"):
        print 2
        #BamAggregator(args.query, args.normal_bam_list, args.tumor_bam_list, args.interval_list)


    if (args.subparser == "variant_assess"):
        print 3
        #VariantAssessor(args.query,args.tsv)

    if (args.subparser == "variant_upload"):
        print 4
        #VariantUploader(args.tsv,submit_to_filesystem=False)

    if (args.subparser == "variant_submit"):
        print 5
        #VariantUploader(args.tsv,submit_to_filesystem=True)

if __name__ == '__main__':
    main()
