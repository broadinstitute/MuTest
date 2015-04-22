
def isIndel(self):
    ref = self.data['ref']
    alt = self.data['alt']

    if 1 < len(ref) == 1 < len(alt):
        raise Exception("IsIndel: ref={ref} alt={alt}".format(ref=ref,alt=alt))

    return len(ref) > 1 or len(alt) > 1


def isSNP(variant):
    ref = variant['ref']
    alt = variant['alt']

    if len(ref) > 1: return False
    if len(alt) > 1: return False

    if alt not in set(['A', 'C', 'G', 'T']): return False

    return True