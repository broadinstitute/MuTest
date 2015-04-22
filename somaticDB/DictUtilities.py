def merge_dicts(dict1, dict2):
	new_dict = {}
	for key in dict1: new_dict[key] = dict1[key]
	for key in dict2: new_dict[key] = dict2[key]
	return new_dict

def clean_up_lists(D):
	for key in D:
		if type(D[key]) == list: D[key] = D[key][0]
	return D

def stringify_dict(D):
	for key in D:
		if type(D[key]) == list:
			D[key] = map(unicode,D[key])
		else:
			D[key] = unicode(D[key])
	return D
