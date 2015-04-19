CURRENT_DIR = "/dsde/working/somaticDB/current"
DEVELOPMENT_DIR = "/dsde/working/somaticDB/development"

GIT_REPOSITORY = "https://github.com/broadinstitute/SomaticDB"

import shutil
import os

class SomaticDatabase:

    def __init__(self, location):
        self.location = location


    def create_directories(self):
        self.code_location = os.join(self.location, "code")
        self.data_location = os.join(self.location, "data")

        for directory in [self.code_location,self.data_location]:
            if not os.path.exists( self.code_location ):
                os.mkdir(directory)

            cmd = "git clone %s %s" %(GIT_REPOSITORY,directory)

            os.system(cmd)

    def hard_reset(self):
        for directory in [self.code_location,self.data_location]:
            shutil.rmtree(directory)

