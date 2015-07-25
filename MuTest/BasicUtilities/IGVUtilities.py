IGV_INTRO="""new
genome hg19
load %(normal_bam)s
load %(tumor_bam)s
snapshotDirectory %(snapshot_dir)s"""

IGV_SNAPSHOT="""goto %(position)S
sort base
collapse
snapshot"""

IGV_END="""exit"""

def igv_script_start(normal_bam,tumor_bam,snapshot_dir):
	return IGV_INTRO%{'normal_bam': normal_bam,
				      'tumor_bam': tumor_bam,
				      'snapshot_dir': snapshot_dir}

def igv_snapshot(position):
	return IGV_SNAPSHOT%{'position':position}
