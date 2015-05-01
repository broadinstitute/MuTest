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
        if isinstance(entry, list): return True
    return False


def flatten(s):
    if isinstance(s,list)|isinstance(s,tuple):
        if contains_a_list(s):
            data = [flatten(entry) for entry in s]
            return list(chain(*data))
        else:
            return s
    else:
        return s


def list_product(*args):
    result = list(product(*args))

    print "product:", result
    print

    result = map(flatten, result)
    result = map(list,result)

    print "chain:", result

    for thing in result:
        print list(thing)

    result = map(list, result)

    print result
    print

    return result

def list_product_drop_none(*args, **kwargs):
    return map(drop_none,list_product(*args, **kwargs))



