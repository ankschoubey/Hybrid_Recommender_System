import core
import generate_defaults
import json

from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import *
from dataset import *
from hybridization import Hybridization
from json_formater import JSON_formatter

from time import time

if not core.file_exists('defaults.json'):
    generate_defaults.generate_defaults()

defaults = core.json_read('defaults.json')

db = Database()

if not db.table_exists('ratings', 'movies', 'links', 'movies_mapped'):
    ml = Movielens_Prepare(defaults['dataset'],db)

ml = Movielens(db)

# recommendation on
movies_id = 7

movie_title = ml.get_movie_names([movies_id]).loc[0,'title']
user_id = 3

print(ml.get_movie_type(movies_id))

start = time()
nb = Normalised_ContentBasedFiltering()
nb.fit(ml.load_complete_movie_info())
fitting = time() - start

print('Fit time = ',fitting)
ncb_recommendation = nb.predict(movies_id)

# for i in range(ml.load_complete_movie_info().shape[0]):
#     ncb_recommendation = nb.predict(i)
print(nb.export())
end =  time()
total_ncb = end - start

# print(ncb_recommendation)

start = time()
cb = Simple_ContentBasedFiltering()
cb.fit(ml.load_complete_movie_info())
fitting = time() - start

print('Fit time = ',fitting)
cb_recommendation = cb.predict(movies_id)[:ncb_recommendation.shape[0]]

#print(cb.export())
exit()
# for i in range(ml.load_complete_movie_info().shape[0]):
#     cb_recommendation = cb.predict(i)[:ncb_recommendation.shape[0]]
end =  time()
total_cb = end - start


#print(cb_recommendation)

print('number of items in simple cb ', cb_recommendation.shape,  'time taken',total_cb)
print('number of items in normalised cb ', ncb_recommendation.shape, 'time taken',total_ncb)
print('number of same items ', np.intersect1d(cb_recommendation,ncb_recommendation).shape)

# Collaborative Filtering

cf = CollaborativeFiltering()
cf.fit(ml.load_ratings())

print('Collaborative Filtering Recommendation for item:',movie_title)
cf_item_recommendation = cf.predict(item_id=movies_id)
print(cf_item_recommendation)

cf_user_recommendation = cf.predict_for_user(user_id = user_id)
print('Collaborative Filtering Recommendation for user:', user_id)
print(cf_user_recommendation)

# Hybridization
print('Mixed Hybridization')

combination = Hybridization.mixed([cb_recommendation,cf_item_recommendation,cf_user_recommendation])
print(combination, type(combination))

# JSON Formatting

recommended = {}

recommended['Recommended for you'] = combination.tolist()
recommended['Because you liked '+movie_title] =cb_recommendation.tolist()
recommended['User who liked '+movie_title+'also liked this']  =cf_user_recommendation.tolist()

formatter = JSON_formatter(db)
json1 = formatter.format(recommended)

json1.replace('\"','\\\"')
parsed = json.loads(json1)

print(json.dumps(parsed, indent=4, sort_keys=True))

# Send json to file

with open('sample.json','w') as file:
   json.dump(parsed, file,indent=4)
