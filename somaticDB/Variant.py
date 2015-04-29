
def isIndel(record):
    ref = record['ref']
    alt = record['alt']

    if 1 < len(ref) == 1 < len(alt):
        raise Exception("IsIndel: ref={ref} alt={alt}".format(ref=ref,alt=alt))

    return len(ref) > 1 or len(alt) > 1


def isSNP(record):
    ref = record['ref']
    alt = record['alt']

    if ref not in set(['A', 'C', 'G', 'T']): return False
    if alt not in set(['A', 'C', 'G', 'T']): return False

    return True