from collections import defaultdict
import csv

import ConfusionMatrix


class ConfusionMatrixManager:

    def __init__(self):
        self.pool = defaultdict(ConfusionMatrix)

    def modify(self, keys = None, value = None,feature = None, action = None):
        if (keys == None) | (None in keys):
            raise Exception("Invalid key (None) used in ConfusionStatistics class")

        for key in keys:
            self.pool[key].modify(self, keys = keys, value = value,feature = feature, action = action)

    def add(self, keys = None, test=None, truth=None):
        if (keys == None) | (None in keys):
            raise Exception("Invalid key (None) used in ConfusionStatistics class")

        for key in keys:
            self.pool[key].add(test=test,truth=truth)

    def __iter__(self):
        return iter(self.pool.keys())

    def __getitem__(self, item):
        return self.pool[item]

    def save(self,filename=None, fieldnames = None):
        file = open(filename,'w')
        writer = csv.DictWriter(file,
                                fieldnames=["collection"]+fieldnames,
                                delimiter='\t')

        writer.writeheader()

        for key in self.pool.keys():
            data_dict = dict([(fieldname,self.pool[key].get(score_type=fieldname)) for\
                        fieldname in fieldnames])

            if isinstance(key,list)|isinstance(key,tuple):
                data_dict["collection"] = " ".join(list(key))
            else:
                data_dict["collection"] = key


            writer.writerow(data_dict)

        file.close()





