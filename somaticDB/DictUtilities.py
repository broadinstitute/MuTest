import csv

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