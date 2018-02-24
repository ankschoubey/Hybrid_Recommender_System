import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pathlib
from functools import reduce
import logging
import datetime
import pytz
import json
import os
# Logging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def get_logger(module_path, file_name = 'execution.log'):
    module_path = module_path.split('/')

    name = module_path[-1]
    current_directory = '/'.join(module_path[:-1])

    directory =  current_directory+'/Logs/'
    directory_maker(directory)
    print(current_directory+'execution.log')
    logging.basicConfig(filename = directory+'execution.log', format = LOG_FORMAT, level=logging.DEBUG)

    logger = logging.getLogger(name)
    return logger

# Computation

def reverse_argsort(arg):
    return np.argsort(arg)[::-1]

def pairwise_cosine(data):
    return cosine_similarity(data)

def file_exists(location):
    path = pathlib.Path(location)
    return path.exists()

def union(lists):
    return reduce(np.union1d, lists)

# Pickle and JSON and File

def directory_maker(path): # makes directory if path does not exists
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_pickle(location):
    with open(location, 'rb') as file:
        #print('Loaded', location)
        return pickle.load(file)

def save_pickle(object, name):
    with open(name, 'wb') as file:
        pickle.dump(object, file)
    print('Saved',name)

def json_read(filename):
    return json.load(open(filename, 'r'))

# other
def current_seconds():
    origin_date = datetime.datetime(1970,1,1,0,0,0,tzinfo=pytz.UTC)
    current_date = datetime.datetime.now()
    our_timezone = pytz.timezone('Asia/Kolkata')
    current_date = our_timezone.localize(current_date)
    return (current_date-origin_date).total_seconds()

