from itertools import product

def drop_none(y):
	return filter(lambda x: x is not None, y)

def list_product(*args, **kwargs):
	return list(product(*args, **kwargs))

def list_product_drop_none(*args, **kwargs):
	return map(drop_none,list_product(*args, **kwargs))