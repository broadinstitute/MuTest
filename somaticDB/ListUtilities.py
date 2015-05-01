from itertools import product , chain

def drop_none(y):
    return filter(lambda x: x is not None, y)

def make_list(x):
    if isinstance(x,list):
        return
    else:
        return [x]


def contains_a_list(s):
    for entry in s:
        print entry
        if isinstance(entry, list): return True
        if isinstance(entry, tuple): return True
    return False


def flatten(s):
    if isinstance(s,list)|isinstance(s,tuple):
        data = [flatten(entry) for entry in s]
        return list(chain(*data))
    else:
        return [s]


def list_product(*args):
    result = list(product(*args))

    result = map(flatten, result)

    result = map(tuple,result)

    return result

def list_product_drop_none(*args, **kwargs):
    return map(drop_none,list_product(*args, **kwargs))



