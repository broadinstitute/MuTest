def merge_dicts(dict1, dict2):
    new_dict = {}
    for key in dict1: new_dict[key] = dict1[key]
    for key in dict2: new_dict[key] = dict2[key]
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
            #D[key] = map(lambda s: drop_weird_characters(str(s)),D[key])
            D[key] = map(unicode,D[key])
        else:
            #D[key] = drop_weird_characters(str(D[key]))
            D[key] = unicode(D[key])
    return D
