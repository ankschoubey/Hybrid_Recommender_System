import json
from sqlalchemy.engine.url import URL
import core

def database(choice):
    postgre = ['username','password','host','port','database']
    db_info = {}
    later_append = ''

    mysql = ['username','password','host','port','database']
    sqlite = ['database']
    db_info = {'drivername': 'postgres'}
    if choice == 1:
        db_list = postgre
        db_info['drivername']='postgres'
    elif choice == 2:
        db_list = mysql
        db_info['drivername']='mysql+mysqldb'
        later_append ='?charset=utf8mb4'
    else:
        db_info['drivername']='sqlite'
        db_list = sqlite


    for i in db_list:
        db_info[i]=input('Enter ' + i)

    return str(URL(**db_info))+later_append

def generate_defaults():

    moviedb_id = input('Enter TheMovieDB API Key:')

    choice = 4

    while choice<1 or choice>3:
        choice = int(input('Enter choice of database\n1. PostGres\n2.MySQL\n3.SQLite\nUse Option 3 if you don\'t have Server Setup\n'))

    sql_defaults = database(choice)

    print(sql_defaults)

    movie_lens_dataset_location = input('\nEnter MovieLens Dataset Location on your computer: ')

    defaults={}
    defaults['moviedb_api_key'] = moviedb_id
    defaults['database'] = sql_defaults
    defaults['dataset'] = movie_lens_dataset_location

    core.save_pickle(defaults,'defaults.pickle')