import numpy as np
import core
from dataset import *

cf_table={'item': 'cf_item_recommendation',
          'user': 'cf_n_similar_users',
          'user_recommendation': 'cf_user_recommendation'
          }
class PrepareCollaborativeFiltering:

    def __init__(self,db):
        self.db = db
        self.ratings = Movielens(db).load_ratings()
        self.limit = 20

        self.generate_user_similarity_matrix()
        self.generate_item_similarity_matrix()

        self.save_complete_item_similarities_to_database()
        self.save_complete_similar_users_to_database()
        self.save_recommendation_for_user()

    # Item Similarity
    def generate_item_similarity_matrix(self):
        data = self.ratings.transpose()
        data[data > 0] = 1
        self.item_similarities = core.pairwise_cosine(data)

    def save_complete_item_similarities_to_database(self):
        similar_movies = []

        for i in range(0, self.ratings.shape[1]):
            predicted = self.predict_by_item_similarirty(i)
            similar_movies.append(predicted)
        df = pd.DataFrame(similar_movies)
        df['id']=df.index
        self.db.save_entire_df(df, cf_table['item'])

    def predict_by_item_similarirty(self, item_id):
        arguments_sorted =  core.reverse_argsort(self.item_similarities[item_id])
        arguments_sorted = arguments_sorted[arguments_sorted != item_id][:self.limit]
        return arguments_sorted

    # User Similarity

    def generate_user_similarity_matrix(self):
        self.user_similarities = core.pairwise_cosine(self.ratings)

    def top_n_similar_users(self,user_id):
        return np.argsort(self.user_similarities[user_id])[::-1][1:11]

    def user_similarity_for_index(self,row, column):
        return self.user_similarities[row, column]

    def save_complete_similar_users_to_database(self):
        values = []

        for i in range(0, self.ratings.shape[0]):
            predicted = self.top_n_similar_users(i)
            similarity = self.user_similarity_for_index(i,predicted)
            user_id = np.array([i for j in range(predicted.shape[0])])
            data = pd.DataFrame([user_id,predicted,similarity])
            data = data.transpose()
            values.append(data)

        df = pd.concat(values)
        renaming = {0: 'id', 1: 'similar_user', 2: 'similarity'}
        df = df.rename(columns = renaming)

        df['id'] = df['id'].astype(int)
        df['similar_user'] = df['similar_user'].astype(int)
        #print(df)
        self.db.save_entire_df(df, cf_table['user'])

    def predict_by_user_similarity(self, user_id):
        top_10_similar_users = np.argsort(self.user_similarities[user_id])[::-1][1:11]

        value = []

        for i in range(self.ratings.shape[0]):
            if self.ratings[user_id,i] != 0:
                value.append(0)
                continue
            weightage_of_item = 0
            for k in top_10_similar_users:
                weightage_of_item+=self.ratings[k,i]*self.user_similarities[user_id,k]

            value.append(weightage_of_item)

        return np.argsort(value)[:self.limit]

    def save_recommendation_for_user(self):
        recommendation = []
        print(self.user_similarities.shape[0])
        for i in range(self.user_similarities.shape[0]):
            print(i)
            prediction = self.predict_by_user_similarity(i)
            recommendation.append(prediction)
        df = pd.DataFrame(recommendation)
        df['id'] = df.index
        print(df)
        self.db.save_entire_df(df, table_name=cf_table['user_recommendation'])

class CollaborativeFiltering:

    def limit_number_of_recommendations(self,limit):
        self.limit = limit


    def reload_conditions(self):
        return not self.db.table_exists(cf_table['user'],cf_table['item'],cf_table['user_recommendation'])

    def __init__(self, db, clear_cache=False):
        self.db = db
        ml = Movielens(db)
        self.user_similarities_table = 'collaborative_user_similarities'

        self.user_recommendation_table = 'collaborative_user_recommendation';

        if self.reload_conditions() or clear_cache:
            PrepareCollaborativeFiltering(db)

    def predict_for_item(self, item_id):
        prediction = self.db.get(cf_table['item'], where = 'id = '+str(item_id))
        prediction = prediction.drop(['index', 'id'], axis=1)
        return prediction.values[0]

    def generate_prediction(self, user_id):
        top_10_similar_users = self.db.get(cf_table['user'], where = 'id = '+ str(user_id))

        top_10_similar_users = top_10_similar_users.drop(['index', 'id'], axis=1)

        similarities = dict(zip(top_10_similar_users['similar_user'].tolist(), top_10_similar_users['similarity'].tolist()))
        # get ratings
        similar_users_ratings = self.db.get('ratings', where = 'userId in ('+','.join(map(str,similarities))+')')
        similar_users_ratings = similar_users_ratings.drop(['index', 'timestamp'], axis=1)

        user_ratings = self.db.get('ratings', where = 'userId = '+str(user_id))

        # remove things which are already rated by the user

        similar_users_ratings = similar_users_ratings[~similar_users_ratings['movieId'].isin(user_ratings['movieId'])]

        movies = similar_users_ratings['movieId'].unique().tolist()

        movie_weightage = []

        for i in movies:
            user_who_have_rated = similar_users_ratings[similar_users_ratings['movieId']==i]

            user_who_have_rated['weightage'] = user_who_have_rated['rating'] * user_who_have_rated['userId'].map(similarities)
            movie_weightage.append([i, user_who_have_rated['weightage'].sum()])

        df = pd.DataFrame(movie_weightage, columns=['id','weightage'])
        df = df.sort_values('weightage', ascending=False)
        return df.head(10)['id'].tolist()

    def predict_for_user(self, user_id):
        recommendation = self.db.get(cf_table['user_recommendation'], where = 'id = '+str(user_id))
        recommendation = recommendation.drop(['index','id'], axis =1)
        return recommendation.values[0]
        # return self.generate_prediction(user_id)
