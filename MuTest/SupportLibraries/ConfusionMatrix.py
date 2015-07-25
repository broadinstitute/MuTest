import numpy as np

class ConfusionMatrix:
    """
    A simple confusion matrix class. It is iterative.
    """
    def __init__(self):
        self.reset()

    @property
    def true_positives(self):
        return self.data[(True,True)]

    @property
    def true_negatives(self):
        return self.data[(False,False)]

    @property
    def false_positives(self):
        return self.data[(True,False)]

    @property
    def false_negatives(self):
        return self.data[(False,True)]

    def modify(self,value = None,feature = None, action = None):
        if feature == "true negative": index=(False,False)
        if feature == "true positive": index=(True,True)
        if feature == "false positive": index=(True,False)
        if feature == "false negative": index=(False,True)

        if action == "set":
            self.data[index]=value
        if action == "add":
            self.data[index]+=value

    @property
    def negatives(self):
        return self.true_negatives + self.false_positives

    @property
    def positives(self):
        return self.true_positives + self.false_negatives

    def reset(self):
        self.data = dict({(True,True):np.nan,(True,False):np.nan,(False,True):np.nan,(False,False):np.nan})

    def add(self,test=None,truth=None):
        if np.isnan(self.data[(test,truth)]):
            self.data[(test,truth)]=1
        else:
            self.data[(test,truth)]+=1

    def get(self,score_type=None):
        TP = float(self.true_positives)
        FP = float(self.false_positives)
        TN = float(self.true_negatives)
        FN = float(self.false_negatives)

        if score_type == 'true positives' : return TP
        if score_type == 'false positives': return FP
        if score_type == 'true negatives' : return TN
        if score_type == 'false negatives': return FN

        if score_type in ['sensitivity','true positive rate','TPR']:
            return TP/(TP+FN)

        if score_type in ['specificity','SPC']:
            return TN/(FP+TN)

        if score_type in ['precision','positive predictive value','PPV']:
            return TP/(TP+FP)

        if score_type in ['false discovery rate','FDR']:
            return FP/(TP+FP)

        if score_type in ['MCC','matthews correlation coefficient']:
            numerator = TP*TN - FP*FN
            denominator = np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
            return numerator/denominator