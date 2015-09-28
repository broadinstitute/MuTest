from collections import defaultdict

def merge_dicts(*dictionaries):
    new_dict = {}

    for dictionary in dictionaries:
        for key in dictionary: new_dict[key] = dictionary[key]

    return new_dict

def clean_up_lists(D):
    for key in D:
        if type(D[key]) == list: D[key] = D[key][0]
    return D

def drop_weird_characters(s):
    return "".join(map(chr,filter(lambda k:k < 128, [ord(c) for c in s])))

def stringify_dict(D):
    for key in D:
        if type(D[key]) == list:
            D[key] = map(lambda s: drop_weird_characters(str(s)),D[key])
        else:
            D[key] = drop_weird_characters(str(D[key]))
    return D


def get_entries_from_dict(D, keys=None,return_type=list):
    if keys is None: keys = D.keys()

    if return_type in [list,set,tuple]:
        result = [D[key] for key in keys]
        return return_type(result)

    if return_type == dict:
       result = [ (key,D[key]) for key in keys]
       return dict(result)

    raise Exception("Type not supported in function get_entries_from_dict: %s" % str(return_type))


def read_dict_from_file(filename,delimiter='\t'):
    """
    Read delimited file and return a dictionary where the first column is the key and the value is a list
    composed of the remaining columns, or a single non-list value if there is only on remaining column.

    :param filename:  The name of the file where the data is stored.
    :param delimiter: The data is assumed to be stored in some delimited tabular form.
    """

    result = {}
    file = open(filename)

    for line in file:
            line = line.strip().split(delimiter)
            key = line[0]
            value = line[1:]

            if len(value) == 1: value = value[0]

            result[key] = value

    return result

def tally(entries):
        result = defaultdict(list)

        for entry in entries:
                key,value = entry
                result[key].append(value)

        return dict(result)