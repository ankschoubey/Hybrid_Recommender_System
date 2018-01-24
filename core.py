import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pathlib
from functools import reduce

def reverse_argsort(arg):
    return np.argsort(arg)[::-1]

def pairwise_cosine(data):
    return cosine_similarity(data)

def file_exists(location):
    path = pathlib.Path(location)
    return path.exists()

def load_pickle(location):
    with open(location, 'rb') as file:
        #print('Loaded', location)
        return pickle.load(file)

def save_pickle(object, name):
    with open(name, 'wb') as file:
        pickle.dump(object, file)
    print('Saved',name)

def list_union(a, b):
    return list(set(a) | set(b))

def union(*lists):
    return reduce(np.union1d, (lists))
'''
def row_wise_argsort_with_index(args, limit=None):
    final_indexes = args.columns.values
    temp = []

    for index,i in args.iterrows():
        a = reverse_argsort(i)


        a = map(final_indexes, a)
        temp.append(a)
        print(a)

    df = pd.DataFrame(temp)
    print(df)

import pandas as pd

df = pd.DataFrame([[10,20,50,40],[30,20,10,5]], columns=[1,2,3,4]);
#print(df)
#print(df.columns.values[1], type(df.columns.values))
row_wise_argsort_with_index(df)

#print(row_wise_argsort_with_index([10,20,30]))
'''