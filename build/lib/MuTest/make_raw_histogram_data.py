import pandas as pd

filename = '/dsde/working/somaticDB/master/records/tcga.tsv'

data = pd.read_csv(filename,sep='\t')

for k,row in data.iterrows():
	print dict(row)

