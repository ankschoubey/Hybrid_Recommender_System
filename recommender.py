import dataset
import numpy as np
import core

from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import ContentBasedFiltering

data = dataset.load_movie_lens('ml-100k/u.data', override=True)

movies_id = [0,1]

cf = CollaborativeFiltering(data)

user_id = 2

#a = cf.predict_by_user_similarity(user_id).tolist()
#print(dataset.get_movie_name([a[0]]))


# = core.list_union(a, b)

c = cf.predict_by_item_similarirty(movies_id[0])
print(c)
cb = ContentBasedFiltering()
item = movies_id[0]
b = cb.predict_by_item_similarirty(item).tolist()
print('Recommendation user ',user_id)
print('Similarity for item',dataset.get_movie_name([item]))

print(b)
a = dataset.get_movie_name(b)
print(a)

a = dataset.get_movie_name(c)
print(a)
c = core.union(b,c)
print('New')
print(c)
a = dataset.get_movie_name(c)
print(a)

#
# a = np.array([1,2,3])
# b = np.array([1,2,4])
# d = np.array([1,2,6])
#
#
# print(c)