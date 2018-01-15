import numpy as np
import core
import dataset

class ContentBasedFiltering:

    def limit_number_of_recommendations(self,limit):
        self.limit = limit

    def __init__(self, all=True, range=[]):
        self.movie_categories = dataset.movie_info()[['Action','Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
       'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]

        self.limit_number_of_recommendations(10)
        self.generate_similarity_matrix()

    def generate_similarity_matrix(self):
        self.item_similarities = core.pairwise_cosine(self.movie_categories)

    def predict_by_item_similarirty(self, item_id):
        return np.argsort(self.item_similarities[item_id])[::-1][:self.limit]

c = ContentBasedFiltering()
predictions = c.predict_by_item_similarirty(0)
