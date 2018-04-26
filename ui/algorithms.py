from ui import core
import pandas as pd
from tqdm import trange
import numpy as np
from scipy.sparse import csr_matrix
import string

class Hybridization:
    def __init__(self):
        pass

    @staticmethod
    def mixed(lists):
        filled_lists = []

        for i in lists:
            try:
                filled_lists.append(list(i))
            except:
                # filter out values that are NONE
                pass

        occurance_count = {}
        for i in filled_lists:
            for j in i:
                occurance_count.setdefault(j,0)
                occurance_count[j]+=1

        unique_items=list(occurance_count.keys())
        occurances=list(occurance_count.values())
        #print(occurance_count)

        results = core.sort_list_using_another(to_sort=unique_items, sort_order=occurances)[::-1]
        #print(results)
        return results
        #return core.union(lists)

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

    def predict_rating(self, test, limit_similar_users=10):

        user_id, item_id = test[0], test[1]

        top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit_similar_users]

        value = []
        weightage_of_item = []
        similarities = []
        for k in top_10_similar_users:
            if self.ratings[k, item_id]:
                temp_weightage = self.ratings[k, item_id] * self.user_similarities[user_id, k]
                #print('weightage',self.ratings[k, item_id],self.user_similarities[user_id, k])
                weightage_of_item.append(temp_weightage)
                similarities.append(self.user_similarities[user_id, k])
        if len(weightage_of_item)==0:
            return 0
        try:
            return int(round(sum(weightage_of_item)/sum(similarities),0))
        except:
            return 0

    def predict_for_user(self, user_id, limit_similar_users=10):
        top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit_similar_users]

        value = []

        for i in range(self.ratings.shape[0]):
            if self.ratings[user_id, i] != 0:
                value.append(0)
                continue
            value.append(self.predict_rating([user_id,i], limit_similar_users=limit_similar_users))

        return core.reverse_argsort(value)

    def export(self, starting_user = 670,limit_columns = 10):
        data = {}
        name = self.__class__.__name__ +'_'

        # Similar Users
        raw = []
        for i in trange(self.user_similarities.shape[0], desc = name+'Similar Users'):
            top_10_similar_users = core.reverse_argsort(self.user_similarities[i])
            raw.append(top_10_similar_users[:limit_columns])

        df = pd.DataFrame(raw)
        df['userId']=df.index.values+starting_user

        data[name+'similar_user'] = df

        # User Based Recommendation
        raw = []
        for i in trange(starting_user,self.user_similarities.shape[0], desc=name+'User Based Recommendation'):
            raw.append(self.predict_for_user(i)[1:limit_columns])

        df = pd.DataFrame(raw)
        df['userId']=df.index.values+starting_user
        data[name+'user_recommendation'] = df


        # Item Based Recommendation
        raw = []
        for i in trange(self.item_similarities.shape[0], desc = name+'Item Based Recommendation'):
            raw.append(self.predict_for_item(i)[:limit_columns])

        df = pd.DataFrame(raw)
        df['movieId']=df.index.values
        data[name+'item_recommendation'] = df

        return data

#from scipy.linalg import svd # ValueError: Sparse matrices are not supported by this function. Perhaps one of the scipy.sparse.linalg functions would work instead.

from scipy.sparse.linalg import svds

class SVD_CollaborativeFiltering:

    def resize_fill_zeros(self,matrix, shape):
        # Make matrix with new shape
        temp = np.zeros((shape[0], shape[1]))

        # Fill the values from original shape
        temp[:matrix.shape[0], :matrix.shape[1]] = matrix
        return temp

    def fit(self, matrix, singular_values = 5):
        matrix = matrix.asfptype()
        self.original_matrix = matrix
        self.matrix_mean = np.mean(self.original_matrix)
        matrix.data -= self.matrix_mean
        #print('Mean',self.matrix_mean)

        self.U , self.s, self.v = svds(matrix, k=singular_values)
        #print('Original Shape', matrix.shape)
        #print('U',self.U.shape)
        #print('S',self.s.shape)
        #print('V',self.v.shape)


        # for multiplication
        # U (m x m) . Sigma (m x n) . V^T (n x n)

        Sigma = np.zeros((matrix.shape[0], matrix.shape[1]))
        #print('Sigma', Sigma.shape)
        Sigma[:self.s.shape[0], :self.s.shape[0]] = np.diag(self.s)


        self.U = self.resize_fill_zeros(self.U, (matrix.shape[0],matrix.shape[0]))
        #self.s = self.resize_fill_zeros(self.s, (matrix.shape[0],matrix.shape[1]))
        self.v = self.resize_fill_zeros(self.v, (matrix.shape[1],matrix.shape[1]))

        self.predicted_matrix = self.U.dot(Sigma.dot(self.v)) + self.matrix_mean

    def recommend(self, user_id):

        ratings_by_user = self.original_matrix[user_id]
        indexes = (ratings_by_user[0]==0).indices
        predictions_at_indexes = self.predicted_matrix[user_id,indexes]

        #print('indexes',indexes)
        #print('predictions',predictions_at_indexes)

        recommendation = core.sort_list_using_another(to_sort=indexes, sort_order=predictions_at_indexes)[::-1]

        return recommendation

    def export(self,  starting_user = 670,limit = 10):
        self.limit = limit
        name = self.__class__.__name__+'_'

        raw = []
        for i in trange(starting_user, self.original_matrix.shape[0], desc=name + ' User Based Recommendation'):
            raw.append(self.recommend(i)[:limit])

        raw = list(map(str,raw))
        data = {}
        df = pd.DataFrame(raw, columns=['recommendation'])
        df['userId'] = df.index.values + starting_user
        data[name + 'user_recommendation'] = df
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


"""
Text Learning
"""

def remove_punctuations(sentence):
    translator = sentence.maketrans('', '', string.punctuation)
    return sentence.translate(translator)

#remove_punctuations('Hello it\,s me!')

class BagOfWords:
    def _add_to_vocabulary(self, words):
        for i in words:
            self.vocabulary[i] = self.word_index
            self.word_index += 1

    def get_words(self, sentence):
        return remove_punctuations(sentence).lower().split(' ')

    def fit(self, text):
        self.vocabulary = {}
        self.word_index = 0
        for i in text:
            words = self.get_words(i)
            words_not_captured = [i for i in words if i not in self.vocabulary]
            self._add_to_vocabulary(words_not_captured)

    def transform(self, text):
        word_matrix = []
        for i in range(len(text)):
            words = self.get_words(text[i])

            unique_words = set(words)

            for j in unique_words:
                count = words.count(j)
                word_matrix.append([i, self.vocabulary[j], count])

        return pd.DataFrame(word_matrix, columns=['sentence', 'word', 'occurance'])

class Bag_of_Words_ContentBasedFiltering:


    def fit(self, movie_titles, minimum_similarity=0.5):
        self.minimum_similarity = minimum_similarity
        movie_titles = movie_titles['title'].values.tolist()
        self.engine = BagOfWords()

        self.engine.fit(movie_titles)
        self.word_vector = self.engine.transform(movie_titles)

        sparse_matrix = csr_matrix((self.word_vector['occurance'], (self.word_vector['sentence'], self.word_vector['word'])))

        self.similar_movies = self.similarity(sparse_matrix)

        return self.similar_movies

    def similarity(self, sparse_matrix):
        similarity = core.pairwise_cosine(sparse_matrix)
        np.fill_diagonal(similarity, 0)

        similar_movies = []
        for i in range(len(similarity)):
            condition_check = similarity[i] > self.minimum_similarity

            similar_names = np.where(condition_check)[0].tolist()
            if len(similar_names):
                similarity_of_names = similarity[i][condition_check].tolist()
                similar_names_sorted = core.sort_list_using_another(to_sort=similar_names, sort_order=similarity_of_names)[::-1]
                similar_movies.append([i,similar_names])
        return pd.DataFrame(similar_movies, columns=['movieId','similar'])
    #
    # def predict(self, item_id):
    #     arguments_sorted = core.reverse_argsort(self.item_similarities[item_id])
    #     # select everything except item_id; else same movie will be recommended
    #     arguments_sorted = arguments_sorted[arguments_sorted!=item_id]
    #     return arguments_sorted
    #

    def trim_by_limit(self, list1):

        if len(list1) > self.limit:
            list1 = list1[:self.limit]
        return list1

    def export(self, limit = 10):
        self.limit = limit
        name = self.__class__.__name__

        similar_movies = self.similar_movies
        similar_movies['similar'] = similar_movies['similar'].map(self.trim_by_limit)
        similar_movies['similar'] = similar_movies['similar'].map(str)

        vocabulary = self.engine.vocabulary
        vocabulary = pd.DataFrame([vocabulary.keys(), vocabulary.values()]).transpose()
        vocabulary.columns = ['word', 'value']

        return {name+'_recommend':similar_movies, name+'_vocabulary':vocabulary, name+'_wordvector':self.word_vector}

    #     raw = []
    #     name = self.__class__.__name__
    #     for i in trange(self.item_similarities.shape[0], desc=name):
    #         raw.append(self.predict(i)[:limit])
    #
    #     df = pd.DataFrame(raw)
    #     df['movieId']=df.index.values
    #     return {name: df}

class Collaborative_Via_Content:

    def fit(self, user_ratings, movie_info):
        self.user_ratings = user_ratings
        self.movie_info = movie_info

        self.generate_all_profiles()
        self.all_profiles = self.all_profiles.fillna(0)
        self.user_similarities = core.pairwise_cosine(self.all_profiles)

    def generate_profile(self, userid):

        # get all movies rated by user and how much they are rated

        user_actions = self.user_ratings[userid]
        movies, ratings = user_actions.indices, user_actions.data

        # Get for each movie get its type matrix and multiply by ratings

        weightage_to_movies = self.movie_info.iloc[movies].multiply(ratings, axis='index')

        # Find sum of all of these

        summation = weightage_to_movies.sum()

        # divide the sum by max value

        max_value = summation.max()

        profile = summation / max_value

        return profile

    def generate_all_profiles(self):

        all_profiles = []
        for i in range(0,self.user_ratings.shape[0]):
            all_profiles.append(self.generate_profile(i))
        self.all_profiles = pd.DataFrame(all_profiles)

        pass

    def recommendation_for_user(self, user_id, limit_similar_users=10):
        #top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit_similar_users]

        value = []

        #items_not_rated_yet = list(np.where(self.ratings[user_id] == 0))
        for i in range(self.user_ratings.shape[0]):
            if self.user_ratings[user_id, i] != 0:
                value.append(0)
                continue
            value.append(self.predict_rating(user_id,item_id=i, limit_similar_users=limit_similar_users))

        return core.reverse_argsort(value)

    def predict_rating(self, user_id,item_id, limit_similar_users=10):
        top_10_similar_users = core.reverse_argsort(self.user_similarities[user_id])[1:limit_similar_users]

        value = []
        weightage_of_item = []
        similarities = []
        for k in top_10_similar_users:
            if self.user_ratings[k, item_id]:
                temp_weightage = self.user_ratings[k, item_id] * self.user_similarities[user_id, k]
                #print('weightage',self.ratings[k, item_id],self.user_similarities[user_id, k])
                weightage_of_item.append(temp_weightage)
                similarities.append(self.user_similarities[user_id, k])
        if len(weightage_of_item)==0:
            return 0
        try:
            return sum(weightage_of_item)/sum(similarities)
        except:
            return 0

    def export(self, starting_user = 670, limit = 10):
        self.limit = limit
        name = self.__class__.__name__

        data = {}

        temp_all_profiles = self.all_profiles
        temp_all_profiles['userId'] = temp_all_profiles.index.values
        all_recommendations = []

        for i in trange(starting_user, self.user_ratings.shape[0], desc=name + ' User Based Recommendation'):
            all_recommendations.append(list(self.recommendation_for_user(i)[:limit]))
        all_recommendations = list(map(str,all_recommendations))

        df = pd.DataFrame(all_recommendations, columns=['recommendation'])
        df['userId'] = df.index.values + starting_user

        return {name+'_userprofile':temp_all_profiles, name+'_user_recommendation':df}
# Evaluation
from sklearn.model_selection import train_test_split
#
class Evaluator:

#     def split_train_test(self, df, test_size):
#         train, test = train_test_split(df, test_size=test_size)
#         return train, test
#
    # def r2(self):
    #     pass

    def rmse(self, actual, predicted):

        temp=[]
        for i,j in zip(actual,predicted):
            temp.append((i-j)**2)

        return np.sqrt(sum(temp))
#     def mean_absolute_error(self):
#         pass
#     def mean_squared_error(self):
#         pass
#
#     def evaluate_collaborative(self, function, test_df, evaluation_method):
