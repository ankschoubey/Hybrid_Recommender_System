import numpy as np
import core
from dataset import *
import pandas as pd
class ContentBasedFiltering:

    def limit_number_of_recommendations(self,limit):
        self.limit = limit

    def __init__(self,db, regenerate = False):
        self.db = db
        self.table = 'content_based_recommendations'

        if regenerate or not db.table_exists(self.table):
            self.generate_similarity_matrix()
            self.limit_number_of_recommendations(20)
            self.store_top_n_similarities_to_database()

    # fetch prediction from database
    def predict(self, item_id):
        prediction = self.db.get(self.table, where='id = ' + str(item_id))
        prediction = prediction.drop(['index', 'id'], axis=1)
        return prediction.values[0]

    # regeneration of similarity matrix
    def generate_similarity_matrix(self):
        ml = Movielens(self.db)
        self.item_similarities = core.pairwise_cosine(ml.load_complete_movie_info())

    def predict_using_similarirty_matrix(self, item_id):
        arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])

        # select everything except item_id; else same movie will be recommended
        arguments_sorted = arguments_sorted[arguments_sorted!=item_id]

        #limit to number of output
        arguments_sorted = arguments_sorted[: self.limit+1]

        return arguments_sorted

    def store_top_n_similarities_to_database(self):
        similar_movies = []
        for i in range(0, self.item_similarities.shape[0]):
            predicted = self.predict_using_similarirty_matrix(i)
            similar_movies.append(predicted)
        df = pd.DataFrame(similar_movies)
        df['id']=df.index
        self.db.save_entire_df(df, self.table)