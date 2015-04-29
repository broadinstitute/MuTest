import argparse
from FileUtilities import is_dir_empty, safe_mkdir, spawn_daemon

HOME_DIR = "/dsde/working/somaticDB/current"
DEVELOPMENT_DIR = "/dsde/working/somaticDB/development"
TEST_DIR = "/dsde/working/somaticDB/test"


GIT_REPOSITORY = "https://github.com/broadinstitute/SomaticDB"

import shutil
import os

class SomaticDatabase:

    def __init__(self, location, branch_name="master"):
        if location == "HOME":
            self.location = HOME_DIR
        elif location == "DEVELOPMENT":
            self.location = DEVELOPMENT_DIR
        elif location == "TEST":
            self.location = TEST_DIR
        else:
            self.location = os.path.abspath(location)

        self.code_location = os.path.join(self.location, "code")
        self.data_location = os.path.join(self.location, "data")
        self.branch_name = branch_name

    def set_branch(self, branch_name):
        self.branch_name = branch_name
        os.chdir(self.code_location)
        cmd = "git checkout %s" % self.branch_name
        os.system(cmd)

    def setup_code_directory(self, branch_name):
        safe_mkdir(self.code_location)

        os.chdir(self.code_location)

        cmd = "git clone %s %s" %(GIT_REPOSITORY,self.code_location)

        if is_dir_empty(self.code_location): os.system(cmd)

        self.set_branch(branch_name)

    def setup_data_directory(self):
        safe_mkdir(self.data_location)

        #TO DO: add the population of the database.

    def setup_directories(self, branch_name):
        self.setup_code_directory(branch_name)
        self.setup_data_directory()

    def soft_reset(self):
        shutil.rmtree(self.code_location)
        self.setup_code_directory(self.branch_name)

    def hard_reset(self):
        for directory in [self.code_location,self.data_location]:
            shutil.rmtree(directory)
        self.setup_directories(self.branch_name)

    def start_database(self, port = 27017):
        if spawn_daemon():
            cmd = "mongod --dbpath %s --port %s" %(self.data_location, str(port))
            os.system(cmd)

def main():
    script_description="""This code provides the main interface for creating, starting and deploying databases.."""
    script_epilog="""Created for evaluation of performance of Mutect 2."""

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                    description=script_description,
                                    epilog=script_epilog,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(help='commands',dest='subparser')

    parser_deploy = subparsers.add_parser('deploy', help='Deploys server.')
    parser_deploy.add_argument('-p','--path', type=str, help='Location of the Server (TEST, DEVELOPMENT, HOME)',metavar='<path>', required=True)
    parser_deploy.add_argument('-b','--branch_name', type=str, help='github branch associated with this database.',metavar='<path>',default="master")

    parser_reset = subparsers.add_parser('refresh', help='Refresh server installation.')
    parser_reset.add_argument('-p','--path', type=str, help='Location of the Server (TEST, DEVELOPMENT, HOME)',metavar='<path>', required=True)
    parser_reset.add_argument('-H','--hard', action='store_true')

    parser_start = subparsers.add_parser('start', help='Starts server.')
    parser_start.add_argument('-p','--path', type=str, help='The path where the server is located.',metavar='<path>',required=True)
    parser_start.add_argument('-P','--port', type=str, help='The port on which the server should be started.',metavar='<port>',default='27017')

    args = parser.parse_args()

    if args.subparser == "deploy":
        D = SomaticDatabase(args.path)
        D.setup_directories(args.branch_name)

    if args.subparser == "refresh":
        D = SomaticDatabase(args.path)
        if args.hard:
            D.hard_reset()
        else:
            D.soft_reset()

    if args.subparser == "start":
        D = SomaticDatabase(args.path)
        D.start_database(port=args.port)

if __name__ == "__main__":
    main()