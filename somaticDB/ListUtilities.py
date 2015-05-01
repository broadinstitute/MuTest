from itertools import product , chain

def drop_none(y):
    return filter(lambda x: x is not None, y)

def list_product(*args, **kwargs):
    result = list(product(*args, **kwargs))
    result = map(chain, result)
    result = map(list, result)
    return result

def list_product_drop_none(*args, **kwargs):
    return map(drop_none,list_product(*args, **kwargs))