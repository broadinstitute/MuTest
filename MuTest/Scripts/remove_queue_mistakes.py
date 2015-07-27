import os

def consistent(filename):
    file = open(filename)

    minimum = 255
    maximum = -255

    for line in file:
        if line.startswith('#'): continue
        line = line.split('\t')

        minimum = min(len(line),minimum)
        maximum = max(len(line),maximum)

    return (minimum == maximum)


def remove_mistakes(directory):

    for filename in os.listdir(directory):
        done_file= os.path.join(directory,"."+filename+".done")
        filename = os.path.join(directory,filename)
        if not filename.endswith('.vcf'): continue

        if not consistent(filename):
            print "broken vcf: "+filename

            os.remove(filename)
            os.remove(done_file)