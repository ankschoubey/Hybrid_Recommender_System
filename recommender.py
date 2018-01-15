from dataset import load_movie_lens
import pandas as pd
import dataset
import numpy as np
import core
from timeit import timeit
from scipy import sparse
import sys

from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import ContentBasedFiltering

data = load_movie_lens('ml-100k/u.data', override=True)

movies_id = [0,1]
print(1)

#cf = CollaborativeFiltering(data)


user_id = 2
#
#a = cf.predict_by_user_similarity(user_id).tolist()
#print(dataset.get_movie_name([a[0]]))
#b = cf.predict_by_item_similarirty(a[0]).tolist()

#c = core.list_union(a, b)
cb = ContentBasedFiltering()
item = 1
b = cb.predict_by_item_similarirty(item).tolist()
#print('Recommendation user ',user_id)
print('Similarity for item',dataset.get_movie_name([item]))

print(b)
a = dataset.movie_info(b)
print(a)