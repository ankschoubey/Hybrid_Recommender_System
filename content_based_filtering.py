import numpy as np
import core
import dataset

class ContentBasedFiltering:

    def limit_number_of_recommendations(self,limit):
        self.limit = limit

    def __init__(self, categories):
        self.movie_categories = categories

        self.limit_number_of_recommendations(10)
        self.generate_similarity_matrix()

    def generate_similarity_matrix(self):
        self.item_similarities = core.pairwise_cosine(self.movie_categories)

    def predict_by_item_similarirty(self, item_id):
        arguments_sorted = np.argsort(self.item_similarities[item_id])[::-1][:self.limit]
        return np.delete(arguments_sorted,[0])