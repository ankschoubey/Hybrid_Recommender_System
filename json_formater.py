from themoviedb import TheMovieDB
from dataset import Database
from core import *
import requests
import pandas as pd
import json
import os

class JSON_formatter:
    def __init__(self,database):
        self.db = database

        self.movie_db = TheMovieDB(load_pickle('defaults.pickle')['moviedb_api_key'])

    def load_into_database(self,id):
        moviedb = TheMovieDB()

    def get_movie_imdb_id(self, ids):
        ids = [str(i) for i in ids]
        return self.db.get(table = 'links', columns=['id', 'imdbId'], where='id in ('+','.join(ids)+')')

    def save_image(self, image_url, path):
        image = requests.get(image_url).content

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'wb+') as file:
            file.write(image)

    def get_from_db(self,id):
        try:
            return self.db.get('movie_info', columns =['id','title','overview','backdrop', 'poster', 'video'], where ='id = '+str(id))
        except:
            self.get_from_api([id])
            return self.db.get('movie_info', columns=['id', 'title', 'overview', 'backdrop', 'poster', 'video'],
                   where='id = ' + str(id))
    def get_from_api(self,ids):
        df = self.get_movie_imdb_id(ids)
        #print(df)
        for index, i in df.iterrows():
            #print(i['imdbId'], '1')
            data = self.movie_db.movie(id=i['imdbId'])
            data['id'] = str(ids[index])
            poster_file_location = 'movie_images/poster/' + data['id'] + '.png'
            if data.get('poster',False):
                self.save_image(data['poster'], poster_file_location)
                print('Downloading poster for ',ids[index])
                data['poster'] = poster_file_location

            backdrop_file_location = 'movie_images/backdrop/' + data['id'] + '.png'
            if data.get('backdrop',False):
                #print(type(data['backdrop']))
                self.save_image(data['backdrop'], backdrop_file_location)
                print('Downloading backdrop for ',ids[index])
                data['backdrop'] = backdrop_file_location

            # data = self.db.get('movie_info', where='id ='+str(i))
            data = pd.DataFrame(data, index=[0])
            self.db.save_entire_df(data, table_name='movie_info', already_exists='append')

    def get_movies_formatted(self, movie_ids):
        df = self.get_movie_imdb_id(movie_ids)
        #print(df)


        #print(df)

        final_list = []

        for index,i in df.iterrows():
            data = self.get_from_db(movie_ids[index])

            if data.empty:
                self.get_from_api([movie_ids[index]])
                data = self.get_from_db(movie_ids[index])

            #print(data)
            #print(data.to_dict().keys())
            temp = {}
            for key, value in data.to_dict().items():
                #print(key,value[0])
                temp[key]= value[0]
            final_list.append(temp)

        return final_list
        # for index, i in df.iterrows():
        #     print(i['imdbId'],'1')
        #     data = self.movie_db.movie(id=i['imdbId'])
        #     data['id'] = str(movie_ids[index])
        #     poster_file_location = 'movie_images/poster/'+data['id']+'.png'
        #     if data['poster']:
        #         self.save_image(data['poster'], poster_file_location)
        #         data['poster'] = poster_file_location
        #
        #     backdrop_file_location = 'movie_images/backdrop/'+data['id']+'.png'
        #     if data['backdrop']:
        #         self.save_image(data['backdrop'], backdrop_file_location)
        #         data['backdrop'] = backdrop_file_location
        #
        #     #data = self.db.get('movie_info', where='id ='+str(i))
        #     data = pd.DataFrame(data, index=[0])
        #     self.db.save_entire_df(data,table_name ='movie_info', already_exists='append')

    def union(self,lists):
        final = set()

        for i in lists:
            for j in i:
                final.add(j)

        return list(final)


    def format(self,dict):
        list_of_lists = list(dict.values())
        all_movies = self.union(list_of_lists)

        print(all_movies)

        movies_formatted = self.get_movies_formatted(all_movies)
        # for i in movies_formatted:
        #     print(i)

        dict['movies'] = movies_formatted
        print(dict.keys())

        return json.dumps(dict)

#a = JSON_formatter(Database())
#b = a.format({'Popular movies':[1,3,4],'Recommender for you:':[10,1,2]})

#print(b)