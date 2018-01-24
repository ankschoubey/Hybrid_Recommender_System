import pandas as pd
import core
import numpy as np
from scipy import sparse
import sqlalchemy

# Force Reset MySQL Password: UPDATE mysql.user SET Password=PASSWORD('root') WHERE User='root';
# users = np.unique(list_of_users)
'''        '''
class Database:
    def __init__(self, user='root', password='',localhost='127.0.0.1',port='3306', database='movielens'):
        # if OperationalError 1045 occurs use no password
        self.engine1 = sqlalchemy.create_engine('mysql+mysqldb://'+user+':'+password+'@'+localhost+':'+port+'/'+database+'?charset=utf8mb4')
        self.engine2 = sqlalchemy.create_engine('mysql+mysqldb://'+user+':'+'root'+'@'+localhost+':'+port+'/'+database+'?charset=utf8mb4')
        print(2)
    def get(self, table, columns = ['*'],where = ''):
        if len(where):
            where= ' WHERE '+where
        query = 'SELECT ' + ','.join(columns) + ' FROM '+table+where
        #print(query)
        try:
            return  pd.read_sql(query, self.engine1)
        except:
            return  pd.read_sql(query, self.engine2)

    def save_entire_df(self, frame, table_name, already_exists = 'replace'):
        try:
            frame.to_sql(table_name, self.engine1, if_exists=already_exists)
        except:
            frame.to_sql(table_name, self.engine2, if_exists=already_exists)

class Movielens_Prepare:
    set_categories = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                      'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
                      'Western', 'no genres listed']

    def __init__(self, source, database):
        self.database = database
        self.source = source
        self.movie_mapping = {} #map movielens movies to our counter
        print('Loading '+self.source)
        self.load_links()
        print('IMDB Links Loaded')

        self.load_ratings()
        print('User Ratings Loaded')

        self.load_movies()
        print('Movies Loaded')
        print('MovieLens Preparation Complete')

    def generate_movie_map(self, df):
        if len(self.movie_mapping)>0:
            return
        mapped = pd.DataFrame({'movieId':df.index.values, 'original_id':df['movieId']})
        self.database.save_entire_df(mapped, 'movies_mapped')
        self.movie_mapping = dict(zip(df['movieId'].tolist(), df.index.values.tolist()))

    def load_links(self):
        df = pd.read_csv(self.source+'/links.csv')
        self.generate_movie_map(df)
        df['movieId'] = df['movieId'].map(self.movie_mapping)
        df = df.rename(columns={'movieId': 'id'})
        self.database.save_entire_df(df, 'links')

    @staticmethod
    def get_movie_catergory_matrix(raw_category):
        this_movie_category = []
        for i in Movielens_Prepare.set_categories:
            if i in raw_category:
                this_movie_category.append(1)
            else:
                this_movie_category.append(0)
        return this_movie_category

    @staticmethod
    def seperate_movie_name_and_year(raw):
        temp = raw.split('(')
        if len(temp[-1]) != 5 or len(temp) == 1:
            return [raw, '']
        #print(temp)

        return [''.join(temp[:-1]), int(temp[-1].replace(')', ''))]

    def load_movies(self):
        df = pd.read_csv(self.source+'/movies.csv')

        # Map original_ids to our_ids
        self.generate_movie_map(df)
        ids = df['movieId'].map(self.movie_mapping)
        # Get matrix of genres
        categories= df['genres'].map(Movielens_Prepare.get_movie_catergory_matrix).tolist()#series to list
        categories= pd.DataFrame(categories, columns=self.set_categories) #conversion from series to dataframe
        categories = categories.rename(columns={'no genres listed': 'unknown', 'Film-Noir': 'Film_Noir', 'Sci-Fi':'Sci_Fi'}) #will cause trouble for SQL

        # Separate movie names and year
        names_and_year = df['title'].map(Movielens_Prepare.seperate_movie_name_and_year).tolist()
        names_and_year = pd.DataFrame(names_and_year, columns=['title', 'year'])

        complete_movies = pd.concat([ids,names_and_year,categories], axis = 1)

        self.database.save_entire_df(complete_movies, 'movies')

    def load_ratings(self,no_of_movies=0, no_of_users=0):
        df = pd.read_csv(self.source+'/ratings.csv')
        df['movieId'] = df['movieId'].map(self.movie_mapping)
        df['userId'] = df['userId'] - 1
        self.database.save_entire_df(df, 'ratings')

        """
        # make_ratings_matrix

        self.rating_matrix = sparse.csr_matrix((df['rating'] , (df['userId'],df['movieId'])))
        array_form = pd.DataFrame(self.rating_matrix.toarray())
        ids = pd.DataFrame(array_form.index.values, columns=['user_id'])
        output = pd.concat([ids, array_form], axis = 1)
        self.similarity_matrix()
        self.database.save_entire_df(output, 'ratings')
        """

class Movielens:
    movie_categories = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                      'Fantasy', 'Film_Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci_Fi', 'Thriller', 'War',
                      'Western', 'unknown']

    def __init__(self, database):
        self.db = database

    def load_ratings(self):
        df = self.db.get(table = 'ratings', columns = ['userId', 'movieID', 'rating'])
        matrix = sparse.csr_matrix((df['rating'], (df['userId'], df['movieID'])))
        return matrix

    def get_movie_names(self, ids):
        ids = list(map(str,ids))
        df = self.db.get(table = 'movies', columns=['title'], where='movieId IN ('+ ','.join(ids)+')')
        return df

    def load_complete_movie_info(self):
        df = self.db.get(table = 'movies', columns = self.movie_categories)
        return df

    def load_selected_movie_info(self, ids):
        ids = list(map(str,ids))
        df = self.db.get(table = 'movies', columns=self.movie_categories, where='movieId IN ('+ ','.join(ids)+')')
        print(df.head())

