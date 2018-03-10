import core
from dataset import *
import pandas as pd
import numpy as np
class Simple_ContentBasedFiltering:

    def fit(self, matrix):
        self.item_similarities = core.pairwise_cosine(matrix)

    def predict(self, item_id):
        arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])

        # select everything except item_id; else same movie will be recommended
        arguments_sorted = arguments_sorted[arguments_sorted!=item_id]

        return arguments_sorted

class Normalised_ContentBasedFiltering:

    similarity_flag = False

    def fit(self, matrix):
        self.normalise_mapper, self.normalised_data = core.normalise_dataframe(matrix)

    def get_movies_of_type(self, movie_type):
        return self.normalise_mapper[self.normalise_mapper['normalised_key'] == movie_type].index.values

    def similar_movies_of_type(self, movie_type):
        similar_movies = core.reverse_argsort(self.normalised_similarity[movie_type])
        return similar_movies

    def predict(self, item_id, limit = 10):
        movie_type = self.normalise_mapper['normalised_key'].iloc[item_id]

        # simple lookup
        selected_movies = self.get_movies_of_type(movie_type)
        selected_movies = selected_movies[np.where(selected_movies != item_id)]
        if selected_movies.shape[0]>limit:
             return selected_movies

        # If don't have the required number of movies of same type, find similar movie_type
        if not self.similarity_flag:
            # since upper part was a simple lookup finding similarity matrix is not compulsary
            self.normalised_similarity = core.pairwise_cosine(self.normalised_data)
            self.similarity_flag = True

        similar_movies = self.similar_movies_of_type(movie_type)

        for i in similar_movies.tolist()[1:]:
            selected_movies = np.append(selected_movies,self.get_movies_of_type(movie_type))
            if selected_movies.shape[0] > limit:
                return selected_movies