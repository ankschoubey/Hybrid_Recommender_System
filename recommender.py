from dataset import *
import numpy as np
import core
from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import ContentBasedFiltering
from hybridization import Hybridization
import generate_defaults
from json_formater import JSON_formatter
import json
import logging

logging.basicConfig(filename = 'execution.log', level = logging.DEBUG)

logging.info('Loading Database Connecter and Movielens')

if not core.file_exists('defaults.pickle'):
    generate_defaults.generate_defaults()

defaults = core.load_pickle('defaults.pickle')

db = Database()

if not db.table_exists(['ratings', 'movies', 'links', 'movies_mapped']):
    ml = Movielens_Prepare(defaults['dataset'],db)

ml = Movielens(db)

# recommendation on
movies_id = 200

movie_title = ml.get_movie_names([movies_id]).loc[0,'title']
user_id = 3

logging.info('Performing Content Based Filtering')

cb = ContentBasedFiltering(db)

print('Content Based Recommendation for', movie_title)
cb_recommendation = cb.predict(movies_id)
print(cb_recommendation)

logging.info('Performing Content Based Filtering')

# Collaborative Filtering

cf = CollaborativeFiltering(db, clear_cache=False)

print('Collaborative Filtering Recommendation for item:',movie_title)
cf_item_recommendation = cf.predict_for_item(movies_id)
print(cf_item_recommendation)

cf_user_recommendation = cf.predict_for_user(user_id)
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
