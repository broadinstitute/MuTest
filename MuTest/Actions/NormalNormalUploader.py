import pandas as pd
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo


def NormalNormalUploader(tsv):
    nn_file = pd.read_csv(tsv,sep='\t')

    collection = connect_to_mongo(collection='NormalNormalData')

    for k,row in nn_file.iterrows():
        fp = open(row['file'])

        collection.remove({'project':row['project'],'dataset':row['dataset']})

        n = 0
        for line in fp:
            n+=1
            line = line.strip()

            data = {'project':row['project'],'dataset':row['dataset'],'sample': str(n), 'file': line}

            collection.insert(data)

        fp.close()