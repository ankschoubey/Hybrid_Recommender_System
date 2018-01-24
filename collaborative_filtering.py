import numpy as np
import core
from dataset import Database
class CollaborativeFiltering:

    def limit_number_of_recommendations(self,limit):
        self.limit = limit

    def __init__(self, ratings, clear_cache=False):
        self.ratings = ratings
        self.limit_number_of_recommendations(10)
        self.generate_user_similarity(clear_cache)
        self.generate_item_similarity(clear_cache)

    def generate_user_similarity(self, clear_cache):
        file_name = 'cf_user_similarity.pickle'
        if not clear_cache and core.file_exists(file_name):
            self.user_similarities = core.load_pickle(file_name)
            return

        self.user_similarities = core.pairwise_cosine(self.ratings)
        #core.save_pickle(self.user_similarities, file_name)

    def generate_item_similarity(self, clear_cache):
        file_name = 'cf_item_similarity.pickle'
        if not clear_cache and core.file_exists(file_name):
            self.item_similarities = core.load_pickle(file_name)
            return
        data = self.ratings.transpose()
        data[data > 0] = 1
        self.item_similarities = core.pairwise_cosine(data)
        #core.save_pickle(self.item_similarities, file_name)

    def predict_by_item_similarirty(self, item_id):
        arguments_sorted =  np.argsort(self.item_similarities[item_id])[::-1][:self.limit]
        return np.delete(arguments_sorted, [0])

    def predict_by_user_similarity(self, user_id):
        top_10_similar_users = np.argsort(self.user_similarities[user_id])[::-1][1:11]

        value = []

        for i in range(self.ratings.shape[0]):
            if self.ratings[user_id,i] != 0:
                continue
            weightage_of_item = 0
            for k in top_10_similar_users:
                weightage_of_item+=self.ratings[k,i]*self.user_similarities[user_id,k]

            value.append(weightage_of_item)

        return np.argsort(value)[:self.limit]

    def update_similarity_matrix(self):
        pass

    def reload_data(self):
        pass