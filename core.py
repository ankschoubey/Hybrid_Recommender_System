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
import pandas as pd
import random

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

def randomly_select_items(array, limit=None):
    if limit:
        return random.choice(array)[:limit]
    return random.choice(array)

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

# Data

# pass in a dataframe, it will return key (normalised keys for original df, normalised dataframe)
# only pass the dataframe with specific columns that needs normalisation
def normalise_dataframe(df):
    original_index = df.index.values

    new_index = []
    count = 0
    normalised_string_list = []
    column_names = df.columns.values

    for index, value in df.iterrows():
        # print(value)
        string_version = str(value.tolist())

        try:
            position = normalised_string_list.index(string_version)
            new_index.append(position)
        except:
            normalised_string_list.append(string_version)
            new_index.append(count)
            count = count + 1

    df['normalised_key'] = new_index

    normalised_list = []

    for i in list(normalised_string_list):
        normalised_list.append(json.loads(i))
    normalised_df = pd.DataFrame(normalised_list, columns=column_names)
    normalised_df['normalised_key'] = normalised_df.index.values

    return pd.DataFrame(df['normalised_key']), normalised_df
