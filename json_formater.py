from themoviedb import TheMovieDB
from dataset import Database
from core import *
import requests
import pandas as pd
import json
import os
import logging

class JSON_formatter:
    def __init__(self,database):
        self.db = database
        self.movie_db = TheMovieDB(json_read('defaults.json')['moviedb_api_key'])

    def get_movie_imdb_id(self, ids):
        ids = [str(i) for i in ids]
        return self.db.get(table = 'links', columns=['id', 'imdbId'], where='id in ('+','.join(ids)+')')

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
            return self.db.get('movie_info', columns =['id','title','overview','backdrop', 'poster', 'video'], where ='id = '+str(id))
        except:
            self.get_from_api([id])
            return self.db.get('movie_info', columns=['id', 'title', 'overview', 'backdrop', 'poster', 'video'],
                   where='id = ' + str(id))

    def get_from_api(self,ids):
        df = self.get_movie_imdb_id(ids)
        for index, i in df.iterrows():
            data = self.movie_db.movie(id=i['imdbId'])
            data['id'] = str(ids[index])
            poster_file_location = 'movie_images/poster/' + data['id'] + '.png'
            if data.get('poster',False):
                print('Downloading poster for ',ids[index])
                self.save_image(data['poster'], poster_file_location)
                data['poster'] = poster_file_location

            backdrop_file_location = 'movie_images/backdrop/' + data['id'] + '.png'
            if data.get('backdrop',False):
                print('Downloading backdrop for ',ids[index])
                self.save_image(data['backdrop'], backdrop_file_location)
                data['backdrop'] = backdrop_file_location

            # updating old record because csv was shitty
            # before: Usual Suspects, The
            # after: The Usual Suspects

            # print('Title is ',data['title'])
            self.db.update(table ='movies', columns = ['title'], values = [data['title']], where='movieId = '+data['id'])

            data = pd.DataFrame(data, index=[0])
            self.db.save_entire_df(data, table_name='movie_info', already_exists='append')

    def get_movies_formatted(self, movie_ids):
        #
        # data_not_in_database = self.db.record_exists(table='movie_info', column='id', values=movie_ids)[1]
        #
        # df = self.get_movie_imdb_id(data_not_in_database)
        #
        # for index, i in df.iterrows():
        #     data = self.get_from_db(movie_ids[index])
        #     if data.empty:
        #          self.get_from_api([movie_ids[index]])
        #          data = self.get_from_db(movie_ids[index])
        #
        #
        final_dict = {}
        df = self.get_movie_imdb_id(movie_ids)
        print(df)

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

        movies_formatted = self.get_movies_formatted(all_movies)
        # for i in movies_formatted:
        #     print(i)

        dict['movies'] = movies_formatted
        #print(dict.keys())

        return json.dumps(dict)
#
# a = JSON_formatter(Database())
# #a.get_from_api([i for i in range(1,100)])
# b = a.format({'Popular movies':[i for i in range(1,300)],'Recommender for you:':[9,3,56]})
# #
# # print(b)