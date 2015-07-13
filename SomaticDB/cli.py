import argparse
from SomaticDB.Actions.VariantUploader import VariantUploader
from SomaticDB.Actions.BamAggregator import BamAggregator
from SomaticDB.Actions.VariantAssessor import VariantAssessor
from SomaticDB.Scripts.clean_database import delete_all


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

    bam_aggregator_parser.add_argument('-f','--folder',
                        help='A folder containing the intervals',
                        type=str,
                        metavar='<older>',
                        required=True)

    bam_aggregator_parser.add_argument('-m','--metadata_list',
                        help='A folder containing the metadata',
                        type=str,
                        metavar='<older>',
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


    database_delete_parser = subparsers.add_parser('database_delete',
                         help  ='Remove all data in the database')

    args = parser.parse_args()

    if (args.subparser == "bam_aggregate"):
        BamAggregator(args.query, args.normal_bam_list, args.tumor_bam_list, args.interval_list,args.metadata_list,args.folder)


    if (args.subparser == "variant_assess"):
        VariantAssessor(args.query,args.tsv)

    if (args.subparser == "variant_upload"):
        VariantUploader(args.tsv,submit_to_filesystem=False)

    if (args.subparser == "variant_submit"):
        VariantUploader(args.tsv,submit_to_filesystem=True)

    if (args.subparser == "database_delete"):
        delete_all()

if __name__ == '__main__':
    main()
