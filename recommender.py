from dataset import *
import numpy as np
import core
from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import ContentBasedFiltering
from hybridization import Hybridization
import generate_defaults
from json_formater import JSON_formatter

if not core.file_exists('defaults.pickle'):
    generate_defaults.generate_defaults()

defaults = core.load_pickle('defaults.pickle')
db = Database()
#ml = Movielens_Prepare(defaults['dataset'],db)
ml = Movielens(db)

movies_id = [0,2]

cf = CollaborativeFiltering(ml.load_ratings(), clear_cache=False)

''' User Based CF
user_id = 2
print('Recommendation user ',user_id)
a = cf.predict_by_user_similarity(user_id).tolist()
print(ml.get_movie_names([a[0]]))
'''
recommended = {}

cb = ContentBasedFiltering(ml.load_complete_movie_info())
item = movies_id[0]
cb_title = ml.get_movie_names([item]).loc[0,'title']
#print(a, type(a))
print('Similarity for item')


print('Content Based Filtering')

b = cb.predict_by_item_similarirty(item).tolist()
print(b)
#a = ml.get_movie_names(b)

#print(a)

print('Collaborative Filtering')
cu = cf.predict_by_user_similarity(1)


cb = cf.predict_by_item_similarirty(movies_id[1])
item = movies_id[1]

cf_title = ml.get_movie_names([item]).loc[0,'title']

#print(c)
#a = ml.get_movie_names(c)
#print(a)

print('Mixed Hybridization')

c = Hybridization.mixed(b,cu,cb)[0]
print(c, type(c))
recommended['Recommended for you'] = c.tolist()
recommended['Because you liked '+cb_title] =b
recommended['User who liked '+cf_title+'also liked this']  =cb.tolist()
#print(recommended)
#a = ml.get_movie_names(c)
#print(a)

formatter = JSON_formatter(db)
json1 = formatter.format(recommended)
print(json1)
import json
parsed = json.loads(json1)
print(json.dumps(parsed, indent=4, sort_keys=True))

with open('sample.json','w') as file:
    json.dump(parsed, file,indent=4)