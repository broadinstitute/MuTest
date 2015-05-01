from itertools import product , chain

def drop_none(y):
    return filter(lambda x: x is not None, y)

def make_list(x):
    if isinstance(x,list):
        return
    else:
        return [x]

def list_product(*args):
    result = list(product(*args))

    print "product:", result
    print

    result = map(lambda x: chain(*x), result)
    result = list(result)

    print "chain:", (result)
    print

    result = map(list, result)

    print result
    print

    return result

def list_product_drop_none(*args, **kwargs):
    return map(drop_none,list_product(*args, **kwargs))