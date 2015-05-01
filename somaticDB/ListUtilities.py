from itertools import product , chain

def drop_none(y):
    return filter(lambda x: x is not None, y)

def list_product(*args, **kwargs):
    result = list(product(*args, **kwargs))

    print result

    result = map(chain, result)

    print result

    result = map(list, result)

    print result

    return result

def list_product_drop_none(*args, **kwargs):
    return map(drop_none,list_product(*args, **kwargs))