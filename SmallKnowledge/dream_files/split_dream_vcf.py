dream_fps=open("/dsde/working/kcarr/kcarr/SmallKnowledge/m2_dream3.fp.intervals",'r')
dream_tps=open("/dsde/working/kcarr/kcarr/SmallKnowledge/m2_dream3.tp.intervals",'r')

filename = "/humgen/gsa-hpprojects/GATK/data/integrationtests/48cb9fbae3ec04514fe8fbf4ff13d586.integrationtest"

fps = set([])
for fp in dream_fps:
	chromosome,position=fp.strip().split(':')
	fps.add((chromosome, position))

tps = set([])
for tp in dream_tps:
        chromosome,position=fp.strip().split(':')
	tps.add((chromosome, position))

file = open(filename)

outfile_false = open("m2_dream3.fp.intervals.vcf",'w')
outfile_true  = open("m2_dream3.tp.intervals.vcf",'w')

for line in file:

	if line.startswith('#'):
		outfile_false.write(line)
		outfile_true.write(line)
		continue

	data = line.strip().split('\t')
	chromosome = data[0]
	position = data[1]
	
	outfile_false.write(line)
	outfile_true.write(line)

outfile_false.close()
outfile_true.close()
