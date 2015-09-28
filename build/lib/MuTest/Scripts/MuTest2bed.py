import sys
import csv

filename = sys.argv[1]

reader = csv.DictReader( open(filename), delimiter ='\t')
writer = csv.DictWriter( open(filename+'.bed','w'), delimiter='\t',fieldnames=['chromosome','start','end','name','score'])

for row in reader:
	writer.writerow({'chromosome': row['chromosome'],
			 'start': row['start'],
			 'end': int(row['start']) + len(row['ref']),
			 'name': str(row['ref']+':'+row['alt'])})
