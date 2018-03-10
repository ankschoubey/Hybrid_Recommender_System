import core

cf_table={'item': 'cf_item_recommendation',
          'user': 'cf_n_similar_users',
          'user_recommendation': 'cf_user_recommendation'
          }

class CollaborativeFiltering:

    def fit(self, ratings):
        # user similarity matrix
        self.user_similarities = core.pairwise_cosine(ratings)

        # item similarity matrix
        data = ratings.transpose()
        data[data > 0] = 1
        self.item_similarities = core.pairwise_cosine(data)

        self.ratings = ratings

    def predict(self, user_id= None, item_id = None, limit = 10):
        if user_id is None and item_id is None:
            raise('No parameter provided for user_id or item_id')
        if user_id:
            return self.predict_for_user(user_id, limit = limit)
        else:
            return self.predict_for_item(item_id, limit = limit)

    def predict_for_item(self, item_id, limit=10):
        arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])
        arguments_sorted = arguments_sorted[arguments_sorted != item_id][:limit+1]
        return arguments_sorted

    def predict_for_user(self, user_id, limit=10):
        top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit+1]

        value = []

        for i in range(self.ratings.shape[0]):
            if self.ratings[user_id, i] != 0:
                value.append(0)
                continue
            weightage_of_item = 0
            for k in top_10_similar_users:
                weightage_of_item += self.ratings[k, i] * self.user_similarities[user_id, k]

            value.append(weightage_of_item)

        return core.reverse_argsort(value)[:limit+1]
