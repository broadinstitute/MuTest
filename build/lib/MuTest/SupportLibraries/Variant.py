
def is_indel(record):
    if is_sv(record): return False

    ref = record['ref']
    alt = record['alt']

    if (ref == '-') | (alt == '-'): return True

    if 1 < len(ref) == 1 < len(alt):
        raise Exception("IsIndel: ref={ref} alt={alt}".format(ref=ref,alt=alt))

    return len(ref) > 1 or len(alt) > 1


def is_snp(record):
    if is_sv(record): return False

    ref = record['ref']
    alt = record['alt']

    if ref not in set(['A', 'C', 'G', 'T']): return False
    if alt not in set(['A', 'C', 'G', 'T']): return False

    return True

def is_sv(record):
    ref = record['ref']
    alt = record['alt']

    if record.has_key("SVTYPE"): return True
    if alt.startswith("<"): return True
    if ref.startswith("<"): return True
    return False

def get_variant_type(record):
    if is_snp(record): return "SNP"
    if is_indel(record): return "INDEL"
    if is_sv(record): return "SV"
    return "UNKNOWN"
