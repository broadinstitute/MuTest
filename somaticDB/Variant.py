class Variant:

    def __init__(self,data):
        self.data = data

    def isIndel(self):
        ref = self.data['ref']
        alt = self.data['alt']
        if 1 < len(ref) == 1 < len(alt):
            raise Exception("IsIndel: ref={ref} alt={alt}".format(ref=ref,alt=alt))
        return len(ref) > 1 or len(alt) > 1