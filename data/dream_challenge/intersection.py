import sys
import vcf
import HTSeq

filename = sys.argv[1]
file = open(filename)
reader = vcf.Reader(file)

for record in reader:
	print record.CHROM, record.POS
	print record.INFO
	print
