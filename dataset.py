import pandas as pd
import core
import numpy as np
from scipy import sparse

def load_movie_lens(location, override = True):
    pickle_file = location+'.pickle'
    if not override and core.file_exists(pickle_file):
        return core.load_pickle(pickle_file)

    file = np.genfromtxt(location, delimiter='\t')

    row = file[:,0]-1
    col = file[:,1]-1
    rating = file[:,2]

    matrix = sparse.csr_matrix((rating, (row, col)))

    core.save_pickle(matrix, pickle_file)
    return matrix

def load_complete_movielens(override = False):
    return load_movie_lens('ml-100k/u.data', override)

def movie_info(ids=0, remake_pickle =False):
    pickle_file = 'u.item.pickle'
    info = None
    if not remake_pickle and core.file_exists(pickle_file):
        info = core.load_pickle(pickle_file)
    else:
        titles = ['id','title', 'release', 'video release','URL','unknown','Action','Adventure','Animation' ,'Children','Comedy','Crime','Documentary','Drama','Fantasy' ,'Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi' ,'Thriller','War','Western']

        info = pd.read_csv('ml-100k/u.item', delimiter='|', encoding='latin-1', names=titles)[:]
        info.dropna(axis=1)
        info.drop(['id','unknown','video release'], axis=1)
        core.save_pickle(info, pickle_file)

    if ids == 0:
        return info
    temp = []
    for i in ids:
        temp.append(info.loc[i])
    return temp
def get_movie_name(ids):
    selected_movie_info = movie_info([ids])
    names = []
    for i in selected_movie_info:
        names.append(i['title'])
    return names

