import os
import argparse

script_description="""A protype script for starting mongoDB server."""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                 description=script_description,
                                 epilog=script_epilog,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-l','--location', help='The location of the server',
                    type=str,metavar='<location>', required=True)

args = parser.parse_args()

locations = {"local": "../srv/",
             "develop":"/dsde/working/somaticDB/develop/data",
             "current":"/dsde/working/somaticDB/current/data"}


cmd = "mongod --dbpath %s" % locations[args.location]

os.system(cmd)
