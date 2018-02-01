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
    ml = Movielens_Prepare(defaults['dataset'],db)

db = Database()
#ml = Movielens_Prepare(defaults['dataset'],db)
ml = Movielens(db)

movies_id = [522,522]

cf = CollaborativeFiltering(db, clear_cache=False)

# # ''' User Based CF
user_id = 2

recommended = {}

cb = ContentBasedFiltering(db)
item = movies_id[0]
cb_title = ml.get_movie_names([item]).loc[0,'title']
#print(a, type(a))
print('Similarity for item')


print('Content Based Filtering')

b = cb.predict(item)
print(b)


print('Collaborative Filtering')

cu = cf.predict_for_user(user_id)

cb = cf.predict_for_item(movies_id[1])
item = movies_id[1]

cf_title = ml.get_movie_names([item]).loc[0,'title']

print('Mixed Hybridization')

print([b,cb,cu])
c = Hybridization.mixed([b,cb,cu])
print(c, type(c))
recommended['Recommended for you'] = c.tolist()
recommended['Because you liked '+cb_title] =b.tolist()
recommended['User who liked '+cf_title+'also liked this']  =cb.tolist()
#print(recommended)
#a = ml.get_movie_names(c)
#print(a)

formatter = JSON_formatter(db)
json1 = formatter.format(recommended)
#print(json1)

print(type(json1))
json1.replace('\"','\\\"')
print(json1)
import json
parsed = json.loads(json1)
print(json.dumps(parsed, indent=4, sort_keys=True))

with open('sample.json','w') as file:
   json.dump(parsed, file,indent=4)