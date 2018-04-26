import generate_defaults
import numpy as np

from ui.data import *
from ui.algorithms import Hybridization, Simple_CollaborativeFiltering, Simple_ContentBasedFiltering, Normalised_ContentBasedFiltering, PopularityBasedFiltering, Bag_of_Words_ContentBasedFiltering, SVD_CollaborativeFiltering, Collaborative_Via_Content,Evaluator

from time import time

"""
This is a sample recommendation file,
Helpful to check if everything is working correctly
"""


""" 1. Get Database Info, TheMovieDB API and Source of MovieLens Dataset """

if not core.file_exists('defaults.json'):
    generate_defaults.generate_defaults()

defaults = core.json_read('defaults.json')


db = Database()

""" 2. If the below table names don't exist in the database, load the dataset into the database """

if not db.table_exists('ratings', 'movies', 'links', 'movies_mapped'):
    ml = Movielens_Prepare(defaults['dataset'],db)

""" 
Movielens() : Will be used to keep algorithms free from datahandling;

This is done so that we can pass any matrix to the algorithm for evaluations. 
"""

ml = Movielens(db)

# recommendation on
movies_id = 8

movie_title = ml.get_movie_names([movies_id]).loc[0,'title']
user_id = 3

print(ml.get_movie_type(movies_id))

"""
# Algorithms

All algorithm classes have these methods
1. fit
2. predict
3. export : core.py has save_exports_to_db function to save all exports to database

read up algorithms.py file to know parameters and output for each class.
"""



"""0. Popularity Based Filtering"""
start = time()
pb = PopularityBasedFiltering()
pb.fit(ml.load_ratings())
#print('prediction is',pb.predict([0,1,3,4,5,1032]))
export = pb.export(custom_field={'action':[1,2,3]})
print(export)
fitting = time() - start
save_exports_to_db(export,db)

print('Fit time Popularity Based Filtering = ',fitting)

""" ContentBasedFiltering: """

""" 1. Normalised_ContentBasedFiltering: """

start = time()
nb = Normalised_ContentBasedFiltering()
nb.fit(ml.load_complete_movie_info())
fitting = time() - start

print('Fit time Normalised_ContentBasedFiltering = ',fitting)
ncb_recommendation = nb.predict(movies_id)[:10]

#save_exports_to_db(nb.export(), db)

end =  time()
total_ncb = end - start

# print(ncb_recommendation)

""" 2. Simple_ContentBasedFiltering: """

start = time()
cb = Simple_ContentBasedFiltering()
cb.fit(ml.load_complete_movie_info())
fitting = time() - start
print('Fit time Simple_ContentBasedFiltering = ',fitting)
cb_recommendation = cb.predict(movies_id)[:ncb_recommendation.shape[0]][:10]
#save_exports_to_db(cb.export(), db)
end =  time()
total_cb = end - start

""" 3. Bag_of_Words_ContentBasedFiltering: """

bag_cb = Bag_of_Words_ContentBasedFiltering()
bag_cb.fit(ml.get_movie_names(), minimum_similarity=0.7)
#export = bag_cb.export()
# for i in export.keys():
#     print(i, export[i])
#save_exports_to_db(export,db)

"""
Both Content Based Filtering Algorithm will product same results
The time taken for Normalised is slow if their is no need to create similarity matrix.
"""


# print('number of items in simple cb ', cb_recommendation.shape,  'time taken',total_cb)
# print('number of items in normalised cb ', ncb_recommendation.shape, 'time taken',total_ncb)
# print('number of same items ', np.intersect1d(cb_recommendation,ncb_recommendation).shape)


""" Collaborative Filtering: """

""" 1. Simple_CollaborativeFiltering : """


cf = Simple_CollaborativeFiltering()
cf.fit(ml.load_ratings())
# for i in range(9000):
#     print(i,cf.predict_rating(0,i))
save_exports_to_db(cf.export(), db)

print('Collaborative Filtering Recommendation for item:',movie_title)
cf_item_recommendation = cf.predict(item_id=movies_id)
#print(cf_item_recommendation)

cf_user_recommendation = cf.predict_for_user(user_id = user_id)
print('Collaborative Filtering Recommendation for user:', user_id)
#print(cf_user_recommendation)

""" 2. SVD_CollaborativeFiltering : """
evaluate = Evaluator()
svd_cf = SVD_CollaborativeFiltering()
svd_cf.fit(ml.load_ratings(), singular_values=300)
#svd_cf_user_recommendation = svd_cf.recommend(0)[:10]
#print('recommendation',svd_cf_user_recommendation)
save_exports_to_db(svd_cf.export(0),db)
#original_list = ml.load_ratings()[1].todense().tolist()[0]
#print(original_list)

#predicted = svd_cf.predicted_matrix[1].tolist()
# print(predicted)
#
# for i, j in zip(original_list, predicted):
#    print(i,j, j-i)
# print('RMSE',evaluate.rmse(actual=original_list,predicted=predicted))

# for i in range(600,680,20):
#     svd_cf.fit(ml.load_ratings(),i)
#     predicted = svd_cf.predicted_matrix[1].tolist()
#
#     constructed_lists_original = []
#     constructed_lists_predicted = []
#
#     for k,j in zip(original_list, predicted):
#         if k !=0:
#             constructed_lists_original.append(k)
#             constructed_lists_predicted.append(j)
#
#     print(i, 'RMSE',evaluate.rmse(actual=constructed_lists_original,predicted=constructed_lists_predicted))



""" Hybridization: """

"""Collaborative Via Content Based"""

cvc = Collaborative_Via_Content()
cvc.fit(ml.load_ratings(), ml.load_complete_movie_info())
#print(cvc.recommendation_for_user(0)[:10])
cvc_user_recommendation = cvc.recommendation_for_user(0)[:10]
export = cvc.export()
save_exports_to_db(export,db)

print('Mixed Hybridization')

combination = Hybridization.mixed([cb_recommendation,cf_item_recommendation,cf_user_recommendation, None])
print(combination, type(combination))

"""
Json Formating:

Not to be used when Django is implemented

Before sending ids to Json_Formatter, limit the number of ids in each category
"""

# recommended = {}
#
# recommended['Recommended for you'] = combination.tolist()[:1000]
# recommended['Because you liked '+movie_title] =cb_recommendation.tolist()[:1000]
# recommended['User who liked '+movie_title+'also liked this']  =cf_user_recommendation.tolist()[:1000]
#
# formatter = JSON_formatter(db)
# json1 = formatter.format(recommended)
#
# #json1.replace('\"','\\\"')
# #parsed = json.loads(json1)
#
# #print(json.dumps(parsed, indent=4, sort_keys=True))
#
# # Send json to file
#
# #with open('sample.json','w') as file:
# #   json.dump(parsed, file,indent=4)
