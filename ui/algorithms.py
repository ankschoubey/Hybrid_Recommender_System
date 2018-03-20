from ui import core
import pandas as pd
from tqdm import trange
import numpy as np

class Hybridization:
    def __init__(self):
        pass

    @staticmethod
    def mixed(lists):
        return core.union(lists)

    def switching(self):
        pass

    def hybridize(self,lists):
        return self.mixed(lists)

class PopularityBasedFiltering:

    def fit(self, ratings):
        # scale rating to be asdbsadlkfasdlk
        # to be made 2.5
        #ratings = ratings.astype(np.float64)

        #ratings[ratings!=0]-=2.5
        #print(ratings)
        self.summation = ratings.sum(axis=0)
        #print(self.summation)


        self.summation = np.array(self.summation)[0]
        #print(self.summation)

        self.overall_popularity = core.reverse_argsort(self.summation)

        self.summation = pd.Series(data=self.summation)
        #print(self.summation)

    #def remap(self, ratings,center = 2.5):


    def predict(self,ids = None, limit=10):

        if ids is None:
            #selected_ids = self.summation
            #print('print',core.reverse_argsort(self.summation.iloc[0].values)[:limit])
            print('ratings')
            print(self.overall_popularity[:limit])
            return self.overall_popularity[:limit]
        #exit()
        selected_ids = self.summation[ids]
        #print(selected_ids)

        #print(selected_ids)
        #print(self.summation.shape[1])
        #not_in_indices = [x for x in range(self.summation.shape[1]) if x not in ids]
        #print(not_in_indices)
        #selected_ids[0, not_in_indices] = 0
        #print(selected_ids)

        indexes = selected_ids.index.values
        #print('index',indexes)

        result = []
        for i in core.reverse_argsort(selected_ids):
            result.append(indexes[i])
            if len(result)>limit:
                break
        return result

    def export(self,custom_field=None,limit_columns=10):
        data = {}
        name = self.__class__.__name__

        df = pd.DataFrame(self.predict(limit=limit_columns))#)#, index=['overall_popular'])
        print(df)
        df = df.transpose()

        categories = ['overall']

        if custom_field != None:
            for key, value in custom_field.items():
                predicted = self.predict(value)

                while len(predicted)<limit_columns:
                    predicted.append(-1)

                df_temp = pd.DataFrame(predicted)#, index=key)
                df_temp = df_temp.transpose()
                print(df_temp)
                df = df.append(df_temp)
                categories.append(key)
        df['categories']= categories
        #df.index.values = [i for i in range(len(df.index.values))]
        data[name] = df
        return data




class Simple_CollaborativeFiltering:

    def fit(self, ratings):
        # user similarity matrix
        self.user_similarities = core.pairwise_cosine(ratings)

        # item similarity matrix
        data = ratings.transpose()
        data[data > 0] = 1
        self.item_similarities = core.pairwise_cosine(data)

        self.ratings = ratings

    def predict(self, user_id= None, item_id = None):
        if user_id is None and item_id is None:
            raise('No parameter provided for user_id or item_id')
        if user_id:
            return self.predict_for_user(user_id)
        else:
            return self.predict_for_item(item_id)

    def predict_for_item(self, item_id):
        arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])
        arguments_sorted = arguments_sorted[arguments_sorted != item_id]
        return arguments_sorted

    def predict_for_user(self, user_id, limit_similar_users=3):
        top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit_similar_users]

        value = []

        for i in range(self.ratings.shape[0]):
            if self.ratings[user_id, i] != 0:
                value.append(0)
                continue
            weightage_of_item = []
            for k in top_10_similar_users:
                weightage_of_item.append(self.ratings[k, i] * self.user_similarities[user_id, k])
            weightage_of_item = sum(weightage_of_item)
            value.append(weightage_of_item)

        return core.reverse_argsort(value)

    def export(self, limit_columns = 10):
        data = {}
        name = self.__class__.__name__ +'_'

        # Similar Users
        raw = []
        for i in trange(self.user_similarities.shape[0], desc = name+'Similar Users'):
            top_10_similar_users = core.reverse_argsort(self.user_similarities[i])
            raw.append(top_10_similar_users[:limit_columns])

        df = pd.DataFrame(raw)
        df['userId']=df.index.values

        data[name+'similar_user'] = df

        # User Based Recommendation
        raw = []
        for i in trange(self.user_similarities.shape[0], desc=name+'User Based Recommendation'):
            raw.append(self.predict_for_user(i)[1:limit_columns])

        df = pd.DataFrame(raw)
        df['userId']=df.index.values
        data[name+'user_recommendation'] = df


        # Item Based Recommendation
        raw = []
        for i in trange(self.item_similarities.shape[0], desc = name+'Item Based Recommendation'):
            raw.append(self.predict_for_item(i)[:limit_columns])

        df = pd.DataFrame(raw)
        df['movieId']=df.index.values
        data[name+'item_recommendation'] = df

        return data

class Simple_ContentBasedFiltering:

    def fit(self, matrix):
        self.item_similarities = core.pairwise_cosine(matrix)

    def predict(self, item_id):
        arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])

        # select everything except item_id; else same movie will be recommended
        arguments_sorted = arguments_sorted[arguments_sorted!=item_id]

        return arguments_sorted

    def export(self, limit = 10):
        raw = []
        name = self.__class__.__name__
        for i in trange(self.item_similarities.shape[0], desc=name):
            raw.append(self.predict(i)[:limit])

        df = pd.DataFrame(raw)
        df['movieId']=df.index.values
        return {name: df}

class Normalised_ContentBasedFiltering:

    similarity_flag = False

    def fit(self, matrix):
        self.normalise_mapper, self.normalised_data = core.normalise_dataframe(matrix)

    def get_movies_of_type(self, movie_type):
        return self.normalise_mapper[self.normalise_mapper['normalised_key'] == movie_type].index.values

    def similar_movies_of_type(self, movie_type):
        similar_movies = core.reverse_argsort(self.normalised_similarity[movie_type])
        return similar_movies

    def create_similarity_matrix(self):
        if not self.similarity_flag:
            self.normalised_similarity = core.pairwise_cosine(self.normalised_data)
            self.similarity_flag = True

    def predict(self, item_id, limit = 10):
        movie_type = self.normalise_mapper['normalised_key'].iloc[item_id]

        # simple lookup
        selected_movies = self.get_movies_of_type(movie_type)
        selected_movies = selected_movies[np.where(selected_movies != item_id)]
        if selected_movies.shape[0]>limit:
             return selected_movies


        # If don't have the required number of movies of same type, find similar movie_type

        # since upper part was a simple lookup, finding similarity matrix is not compulsary
        self.create_similarity_matrix()

        similar_movies = self.similar_movies_of_type(movie_type)

        for i in similar_movies.tolist()[1:]:
            selected_movies = np.append(selected_movies,self.get_movies_of_type(movie_type))
            if selected_movies.shape[0] > limit:
                return selected_movies

    def export(self,limit=10):
        self.create_similarity_matrix()

        raw = []
        for i in range(self.normalised_similarity.shape[0]):
            raw.append(self.similar_movies_of_type(i)[:limit])

        df = pd.DataFrame(raw)
        df['movieId']=df.index.values

        name = self.__class__.__name__ +'_'

        self.normalise_mapper['movieId'] = self.normalise_mapper.index.values

        return {name+'map': self.normalise_mapper, name+'data':self.normalised_data, name+'similarity': df}
