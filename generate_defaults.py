import json
from sqlalchemy.engine.url import URL
import os

def database():
    print('Enter info about SQL database:')
    mysql = ['username','password','host','port','database']

    db_info = {'drivername': 'mysql+mysqldb'}
    later_append ='?charset=utf8mb4'

    for i in mysql:
        db_info[i]=input('Enter ' + i+': ')

    url1 = str(URL(**db_info))+later_append

    db_info['password'] = ''

    url2 = str(URL(**db_info))+later_append

    return (url1,url2)

def get_themoviedb_api():
    api = input('\nGet your API Key from: https://www.themoviedb.org/settings/api\nThen enter TheMovieDB API Key here: ')

    while(len(api))!=32:
        api = input('\nInvalid API Key. Need 32 characters.\nEnter Valid TheMovieDB API Key here:')
    return api

def get_dataset():
    valid = False
    files = ['ratings.csv', 'movies.csv', 'links.csv', 'tags.csv']
    while not valid:
        valid = True
        path = input('\nEnter MovieLens Dataset Location on your computer: ')
        for i in files:
            if not os.path.exists(path+'/'+i):
                valid = False
                print('Could not found:',path+'/'+i)
                break
    return path

def generate_defaults():

    moviedb_id = get_themoviedb_api()

    sql_defaults = database()

    movie_lens_dataset_location = input('\nEnter MovieLens Dataset Location on your computer: ')

    defaults={}
    defaults['moviedb_api_key'] = moviedb_id
    defaults['database'] = sql_defaults
    defaults['dataset'] = movie_lens_dataset_location

    with open('defaults.json','w') as file:
        json.dump(defaults, file, indent=4)

if __name__ == "__main__":
    generate_defaults()