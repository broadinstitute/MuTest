import pandas as pd
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo


def NormalNormalUploader(tsv):
	nn_file = pd.read_csv(tsv,sep='\t')

	collection = connect_to_mongo(collection='NormalNormalData')

	for k,row in nn_file.iterrows():
		fp = open(row['file'])

		for line in fp:
			line = line.strip()

			data = {'project':row['project'],'dataset':row['dataset'],'sample':row['sample'], 'file': line}

			print data

			collection.insert(data)

		fp.close()