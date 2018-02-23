import requests
import json
import core
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