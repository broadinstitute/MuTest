import argparse
from MuTest.Actions.AssessmentFileCreator import create_assessment_file
from MuTest.Actions.NormalNormalAggregator import NormalNormalAggregator
from MuTest.Actions.NormalNormalUploader import NormalNormalUploader
from MuTest.Actions.SurveyDatabase import survey
from MuTest.Actions.VariantUploader import VariantUploader
from MuTest.Actions.BamAggregator import BamAggregator
from MuTest.Actions.VariantAssessor import VariantAssessor
from MuTest.Scripts.clean_database import delete_all
from MuTest.Actions.VariantExtract import variant_extract
from MuTest.Scripts.remove_queue_mistakes import remove_mistakes

import logging


def setup_logging(log_filename):

    loggingFormat = '%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=loggingFormat)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(loggingFormat)
    ch.setFormatter(formatter)

    logging.getLogger('').addHandler(ch)


def main():
    import sys

    print sys.argv


    description = """\nMuTest is a python package for interacting with a mongo database that stores somatic variants. It provides a centralized way of benchmarking the perfomance of algorithms which either generate or refine somatic variant calls.."""

    epilog = """Created for the DSDE methods group to assess mutect 2.\n\n"""

    parser = argparse.ArgumentParser(description=description,
                     epilog=epilog,
                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(help='commands',dest='subparser')

    assessment_file_create_parser = subparsers.add_parser('assessment_file_create',
                    help  ='Creates the file used for assessment of algorithmic results')


    remove_queue_merge_mistakes_parser = subparsers.add_parser('remove_queue_merge_mistakes',
                         help  ='Queue sometimes mangles vcfs. This command removes those bad files.')

    remove_queue_merge_mistakes_parser.add_argument('-d','--directory',
                                                    help='Directory containing vcfs of interest.',
                                                    type=str,metavar='<directory>',required=True)


    bam_aggregator_parser = subparsers.add_parser('bam_aggregate',
                         help  ='Produces a list of bams matching some criteria for an evaluation.')

    normal_normal_uploader_parser = subparsers.add_parser('normal_normal_uploader',
                         help  ='Upload normal-normal data to mongo database.')

    normal_normal_uploader_parser.add_argument('-t','--tsv', help='The lists of normals to be uploaded.',type=str,metavar='<tsv>',required=True)


    survey_parser = subparsers.add_parser('survey',
                                        help  ='Surveys database.')

    survey_parser.add_argument('-o','--output',
                                      help='File where the results should be stored',
                                      type=str,metavar='<output>', required=True)


    normal_normal_collector_parser = subparsers.add_parser('normal_normal_collector',
                                        help  ='Collects bams for normal-normal execution.')

    normal_normal_collector_parser.add_argument('-q','--query',
                                                help='The query for the dataset needed',
                                                type=str,metavar='<query>', required=True)

    normal_normal_collector_parser.add_argument('-o','--output_file',
                                                help='The name of the file to be outputted.',
                                                type=str,metavar='<tsv>', required=True)


    normal_normal_collector_parser.add_argument('-n','--normal_bam_list',
                        help='The name of the normal bam list to be created.',
                        type=str,
                        metavar='<normal_bam_list>',
                        required=True)

    normal_normal_collector_parser.add_argument('-t','--tumor_bam_list',
                        help='The name of the tumor bam list to be created.',
                        type=str ,
                        metavar='<tumor_bam_list>',
                        required=True)





    bam_aggregator_parser.add_argument('-q','--query',
                        help='The query needed to generate the bam lists for evaluation.',
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
                        help='A folder for storing the interval files.',
                        type=str,
                        metavar='<folder>',
                        required=True)

    bam_aggregator_parser.add_argument('-m','--metadata_list',
                        help='A file containing the metadata',
                        type=str,
                        metavar='<metadata_list>',
                        required=True)

    database_delete_parser = subparsers.add_parser('database_delete',
                         help  ='Remove all data in the database. WARNING: ONLY FOR INTERNAL USE.')


    variant_assessor_parser = subparsers.add_parser('variant_assess',
                         help  ='Assesses a file containing variants against truth data stored in the mongo database.')

    variant_extract_parser = subparsers.add_parser('variant_extract',
                         help  ='Saves output from a database query to a file or prints the results to screen.')


    variant_assessor_parser.add_argument('-t','--tsv', help='The list of datasets to be assessed.',type=str,metavar='<tsv>', required=True)
    variant_assessor_parser.add_argument('-q','--query', help='The query for the dataset needed',type=str,metavar='<query>', required=True)
    variant_assessor_parser.add_argument('-o','--output_file', help='The name of the file to be outputted.',type=str,metavar='<tsv>', required=True)
    variant_assessor_parser.add_argument('-d','--outdir', help='The name of the file to be outputted.',type=str,metavar='<tsv>', default="")


    variant_uploader_parser = subparsers.add_parser('variant_upload',
                         help  ="Uploads data to the mongo database. WARNING: ONLY FOR INTERNAL USE. If you are an external user, please use 'variant_submit' instead")


    variant_uploader_parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)


    variant_submitter_parser = subparsers.add_parser('variant_submit',
                         help  ='Sumbits data both to the mongo database and stores information on the filesystem (at /dsde/working/mutestdb)')


    variant_submitter_parser.add_argument('-t','--tsv', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)


    variant_submitter_parser.add_argument('-a','--author', help='The list of datasets to be uploaded.',type=str,metavar='<tsv>',required=True)







    assessment_file_create_parser.add_argument('-t','--tsv',
                                               help='The list of datasets originally submitted to the bam aggregator.',
                                               type=str,
                                               metavar='<tsv>',
                                               required=True)

    assessment_file_create_parser.add_argument('-r','--results',
                                               help='A list of all files created by the test algorithm in the same order as bams.',
                                               type=str,
                                               metavar='<results>',
                                               required=True)

    assessment_file_create_parser.add_argument('-o','--output_file',
                                               help='The name of the assessment file to be created.',
                                               type=str,
                                               metavar='<output_file>',
                                               required=True)

    assessment_file_create_parser.add_argument('-e','--evaluation_rules',
                                               help='Rules for how to treat evidence in the mutestDB. eg. "CM" for confusion matrix or "NN" for normal-normal calling',
                                               type=str,
                                               metavar='<evaluation_rules>')





    variant_extract_parser.add_argument('-o','--output_filename',
                                        help='The file to which the results are mapped.',
                                        type=str,
                                        default='<stdout>',
                                        metavar='<output_filename>')

    variant_extract_parser.add_argument('-m','--max_number_of_records',
                                        help='The max number of records to be outputted.',
                                        type=str,
                                        metavar='<max_number_of_records>',
                                        default = None)


    variant_extract_parser.add_argument('-q','--query',
                                        help='The query needed to generate the bam lists.',
                                        type=str,metavar='<query>',
                                        required=True)

    args = parser.parse_args()

    setup_logging('test.log')

    if (args.subparser == "bam_aggregate"):
        BamAggregator(args.query, args.normal_bam_list, args.tumor_bam_list, args.interval_list,args.metadata_list,args.folder)


    if (args.subparser == "variant_assess"):
        VariantAssessor(args.query,args.tsv,args.output_file,outdir=args.outdir)

    if (args.subparser == "variant_upload"):
        VariantUploader(args.tsv,submit_to_filesystem=False)

    if (args.subparser == "variant_submit"):
        VariantUploader(args.tsv,submit_to_filesystem=True)

    if (args.subparser == "database_delete"):
        delete_all()

    if (args.subparser == "normal_normal_uploader"):
        NormalNormalUploader(args.tsv)


    if (args.subparser == "normal_normal_collector"):
        NormalNormalAggregator(args.normal_bam_list,args.tumor_bam_list,args.query, args.output_file)

    if (args.subparser == "assessment_file_create"):
        create_assessment_file(args.tsv, args.results, args.output_file, args.evaluation_rules)

    if (args.subparser == "variant_extract"):
        variant_extract(args.query, args.output_filename, args.max_number_of_records)

    if (args.subparser == "remove_queue_merge_mistakes"):
         remove_mistakes(args.directory)

    if (args.subparser == "survey"):
         survey(args.output)

if __name__ == '__main__':
    main()
