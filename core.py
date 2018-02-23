import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pathlib
from functools import reduce
import logging
import datetime
import pytz
import json

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

def union(lists):
    return reduce(np.union1d, lists)

def current_seconds():
    origin_date = datetime.datetime(1970,1,1,0,0,0,tzinfo=pytz.UTC)
    current_date = datetime.datetime.now()
    our_timezone = pytz.timezone('Asia/Kolkata')
    current_date = our_timezone.localize(current_date)
    return (current_date-origin_date).total_seconds()

def json_read(filename):
    return json.load(open(filename, 'r'))