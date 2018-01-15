import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pathlib

def reverse_argsort(arg):
    return np.argsort(arg)[::-1]

def pairwise_cosine(data):
    return cosine_similarity(data)

def file_exists(location):
    path = pathlib.Path(location)
    return path.exists()

def load_pickle(location):
    with open(location, 'rb') as file:
        print('Loaded', location)
        return pickle.load(file)

def save_pickle(object, name):
    with open(name, 'wb') as file:
        pickle.dump(object, file)
    print('Saved',name)

def list_union(a, b):
    return list(set(a) | set(b))