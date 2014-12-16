import pandas as pd
import numpy as np

"""
Itemset finder

^\s+([01]\s+){1}1\s+([01]\s+){4}1
"""



def jaccard(a,b):
    _11 = 0
    _not00 = 0
    for x,y in zip(a,b):
        if x and y:
            _11 += 1
            _not00 += 1
        elif x or y:
            _not00 += 1
    return float(_11)/float(_not00)

"""
Use of jaccard:
for i1 in range(5):
    for i2 in range(5):
        if i1 >= i2:
            continue
        print i1+1, i2+1, 1 - jaccard(_ns[i1], _ns[i2])
"""


def gini(vec):
    # It is 1 minus the sum over i of p_i^2, where p_i is the fraction of records belonging to class i.
    asseries = pd.Series(vec)
    valc = asseries.value_counts()
    normed = valc / len(vec)
    powered = normed * normed
    summed = powered.sum()
    return (1 - summed)

def classification_error(vec):
    return 1 - float(pd.Series(vec).value_counts()[0])/len(vec)

def purity_gain(parent, children, measure_method=gini):
    """
    Usage: purity_gain([1,0,1,0], [[0,0],[1,1]], gini)
    """
    # break early:
    children[0][1] # breaks if you're e.g. just passing a 1d list of chars
    #It is the impurity of the parent minus the sum over i of 
    #   (the number of records associated with the child node i divided by the total number of records in the parent node, 
    #   multiplied by the impurity measure of the child node i)
    pval = measure_method(parent)
    pl = float(len(parent))
    chvals = [measure_method(x) * len(x) / pl for x in children]
    
    return pval - sum(chvals)


def least_square(A, y):
    """
    Intercept is placed first
    """
    A = np.vstack([np.ones(len(A)), A]).T
    return np.linalg.lstsq(A, y)[0]

def standardise(vec, ddof=0):
    """
    subtract mean, then divide by standard deviation
    ddof is used as N - ddof in the divisor in std
    """
    vm = np.mean(vec)
    vs = np.std(vec, ddof=ddof)
    return [(x - vm)/vs for x in vec]