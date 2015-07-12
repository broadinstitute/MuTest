import pandas as pd
from cStringIO import StringIO
import os


class SubmissionFile(object):
    def __init__(self,filename):
        if isinstance(filename,list):
            frames = map(lambda d: pd.read_csv(d,sep='\t'),filename)
            self.data = pd.concat(frames).reset_index(drop=True)
        else:
            self.data = pd.read_csv(filename,sep='\t')

    def change_file_dir(self,directory):
        n = len(self.data)
        for k in range(n):
            filename = self.data.ix[k,'data_filename']
            basename = os.path.join(directory,os.path.basename(filename))
            project = self.data.ix[k,'project']
            dataset = self.data.ix[k,'dataset']

            self.data.ix[k,'data_filename'] =\
                "/dsde/working/somaticDB/master/data/%s/%s/"%(project,dataset)

    def fp(self):
        text = StringIO()
        self.data.to_csv(text,sep='\t',index=False)
        text.seek(0)
        return text

    def to_csv(self,filename):
        self.data.to_csv(filename,sep='\t',index=False)