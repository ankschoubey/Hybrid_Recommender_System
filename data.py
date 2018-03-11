import pandas as pd
import core
from scipy import sparse
import sqlalchemy
from sqlalchemy.engine.reflection import Inspector
import requests
import json
import os

class Database:
    def __init__(self):
        self.engine1, self.engine2 =  core.json_read('defaults.json')['database']
        self.engine1, self.engine2 = sqlalchemy.create_engine(self.engine1), sqlalchemy.create_engine(self.engine2)

    def __str__(self):
        return 'Engine 1: '+str(self.engine1)+'\nEngine 2: '+str(self.engine2)

    def get(self, table, columns = ['*'],where = ''):
        if len(where):
            where= ' WHERE '+where
        query = 'SELECT ' + ','.join(columns) + ' FROM '+table+where
        #print(query)
        try:
            return  pd.read_sql(query, self.engine1)
        except sqlalchemy.exc.OperationalError:
            try:
                return  pd.read_sql(query, self.engine2)
            except sqlalchemy.exc.OperationalError as e:
                print(e)
                exit()

    def save_entire_df(self, frame, table_name, already_exists = 'replace', django_pk=True):
        try:
            frame.to_sql(table_name, self.engine1, if_exists=already_exists)
        except:
            frame.to_sql(table_name, self.engine2, if_exists=already_exists)

        if already_exists == 'replace':
            self.set_primary_key_for_django(table_name)

    def set_primary_key_for_django(self, table_name):
        sql = """ALTER TABLE `"""+table_name+ """` 
                ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST,
                ADD PRIMARY KEY (`id`);"""
        try:
            self.engine1.execute(sql)
        except:
            self.engine2.execute(sql)

    def update(self, table, columns,values,where):
        mapping = []

        for k,v in zip(columns, values):
            #print(type(v))
            if type(v) == str:
                v = '"'+v+'"'
            mapping.append(k+' = ' + v)
        sql = 'UPDATE '+table+' SET ' +','.join(mapping)+ ' WHERE '+where+';'
        #print(sql)
        try:
            self.engine1.execute(sql)
        except:
            self.engine2.execute(sql)

    def table_exists(self,*table_name):
        try:
            inspector = Inspector.from_engine(self.engine1)
        except:
            inspector = Inspector.from_engine(self.engine2)
        for i in list(table_name):
            if i not in inspector.get_table_names():
                return  False
        return True

    def record_exists(self,table, column, values):
        if type(values) is not list:
            values = [list]

        exists = []
        does_not_exist = []

        for i in values:
            answer=self.get(table, ['count('+column+')'], where=column + '= '+str(i)).iloc[0,0]

            if answer == 1:
                exists.append(i)
            else:
                does_not_exist.append(i)

        return exists,does_not_exist


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
        #df = df.rename(columns={'movieId': 'id'})
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
        df['rating'] = df['rating'].astype(int)
        self.database.save_entire_df(df, 'ratings')

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

    def get_movie_type(self, id):
        id = str(id)
        df = self.db.get(table = 'movies', columns = self.movie_categories, where='movieId IN ('+ id +')')
        return df.columns[(df != 0).all()].tolist()

    def load_complete_movie_info(self):
        df = self.db.get(table = 'movies', columns = self.movie_categories)
        return df

    def load_selected_movie_info(self, ids):
        ids = list(map(str,ids))
        df = self.db.get(table = 'movies', columns=self.movie_categories, where='movieId IN ('+ ','.join(ids)+')')
        print(df.head())


def save_exports_to_db(data, db):
    for key, value in data.items():
        #print(key, value)
        db.save_entire_df(table_name=key, frame=value)

class TheMovieDB:

    image_path = 'https://image.tmdb.org/t/p/w500'

    def __init__(self,API_Key=None):
        if API_Key:
            self.API_Key = API_Key
        else:
            self.API_Key = core.json_read('defaults.json')['moviedb_api_key']

    @staticmethod
    def format_id(raw_id):
        raw_id = str(raw_id)
        length = len(raw_id)
        if length == 9:
            return raw_id

        while len(raw_id) <7:
            raw_id = '0'+raw_id

        raw_id = 'tt'+raw_id
        return raw_id

    def movie(self,id):
        id = TheMovieDB.format_id(id)

        url = 'https://api.themoviedb.org/3/find/'+id+'?api_key='+self.API_Key +'&language=en-US&external_source=imdb_id'
        a = requests.get(url)
        movie = json.loads(a.content)['movie_results'][0]

        info = {}
        info['title'] = movie['title']
        info['overview'] = movie['overview']
        if movie['poster_path']:
            info['poster'] = self.image_path + movie['poster_path']
        if movie['backdrop_path']:
            info['backdrop'] = self.image_path + movie['backdrop_path']
        info['video'] = movie['video']

        return info

class JSON_formatter:
    def __init__(self,database):
        self.db = database
        self.movie_db = TheMovieDB(core.json_read('defaults.json')['moviedb_api_key'])

    def get_movie_imdb_id(self, ids):
        ids = [str(i) for i in ids]
        #print(self.db)


        return self.db.get(table = 'links', columns=['movieId', 'imdbId'], where='movieId in ('+','.join(ids)+')')

    #needs multi treading
    def save_image(self, image_url, path):
        image = requests.get(image_url).content

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'wb+') as file:
            file.write(image)

    def get_from_db(self,id):
        try:
            return self.db.get('movie_info', columns =['movieId','title','overview','backdrop', 'poster', 'video'], where ='movieId = '+str(id))
        except:
            self.get_from_api([id])
            return self.db.get('movie_info', columns=['movieId', 'title', 'overview', 'backdrop', 'poster', 'video'],
                   where='movieId = ' + str(id))

    def get_from_api(self,ids):
        df = self.get_movie_imdb_id(ids)
        for index, i in df.iterrows():
            data = self.movie_db.movie(id=i['imdbId'])
            data['movieId'] = str(ids[index])
            poster_file_location = 'movie_images/poster/' + data['movieId'] + '.png'
            if data.get('poster',False):
                print('Downloading poster for ',ids[index])
                self.save_image(data['poster'], poster_file_location)
                data['poster'] = poster_file_location

            backdrop_file_location = 'movie_images/backdrop/' + data['movieId'] + '.png'
            if data.get('backdrop',False):
                print('Downloading backdrop for ',ids[index])
                self.save_image(data['backdrop'], backdrop_file_location)
                data['backdrop'] = backdrop_file_location

            # updating old record because csv was shitty
            # before: Usual Suspects, The
            # after: The Usual Suspects

            # print('Title is ',data['title'])
            self.db.update(table ='movies', columns = ['title'], values = [data['title']], where='movieId = '+data['movieId'])

            data = pd.DataFrame(data, index=[0])
            self.db.save_entire_df(data, table_name='movie_info', already_exists='append')

    def get_movies_formatted(self, movie_ids):

        final_dict = {}
        df = self.get_movie_imdb_id(movie_ids)

        for index,i in df.iterrows():
            data = self.get_from_db(movie_ids[index])

            if data.empty:
                self.get_from_api([movie_ids[index]])
                data = self.get_from_db(movie_ids[index])

            temp = {}
            for key, value in data.to_dict().items():
                temp[key]= value[0]
            final_dict[movie_ids[index]] =temp

        return final_dict

    def union(self,lists):
        final = set()

        for i in lists:
            for j in i:
                final.add(j)

        return list(final)

    def format(self,dict):
        list_of_lists = list(dict.values())
        all_movies = self.union(list_of_lists)
        #print('get movies')
        movies_formatted = self.get_movies_formatted(all_movies)
        # for i in movies_formatted:
        #     print(i)

        dict['movies'] = movies_formatted
        #print(dict.keys())

        return json.dumps(dict)