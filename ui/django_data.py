from .models import Ratings
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Count
from .models import NormalisedContentbasedfilteringMap, NormalisedContentbasedfilteringSimilarity, SimpleCollaborativefilteringItemRecommendation, SimpleCollaborativefilteringUserRecommendation, SimpleContentbasedfiltering
from .data import JSON_formatter, Movielens

formatter = JSON_formatter()
movie_lens = Movielens()
numeric_values = [ 'number_0', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'number_6', 'number_7', 'number_8', 'number_9']


def delete_rating(userid, movieid):
    Ratings.objects.filter(userid=userid, movieid=movieid).delete()

def insert_update_rating(userid, movieid,rating,timestamp):
    obj, created = Ratings.objects.update_or_create(
        userid=userid, movieid=movieid,
        defaults={'rating': rating, 'timestamp':timestamp,},
    )


def popularity(filter = False):
    if not filter:
        items = list(Ratings.objects.all().annotate(Avg('rating'), no_of_ratings = Count('rating')).order_by('-no_of_ratings')[:10].values())
        items = [int(i['movieid']) for i in items]
        return items
    else:
        items = list(Ratings.objects.all().annotate(Avg('rating'), no_of_ratings = Count('rating')).order_by('-no_of_ratings')[:10].values())

    items = [int(i['movieid']) for i in items]
    return items
def ratings_for_movie(movieid):
    item = list(Ratings.objects.filter(movieid=movieid).values('movieid').annotate(avg_rating=Avg('rating'),
                                                               no_of_ratings=Count('rating')).order_by('-no_of_ratings',
                                                                                                       '-avg_rating').values())
    return str(item) #{'id': movieid,'no_of_ratings': int(item['no_of_ratings']),'avg_rating': int(item['avg_rating'])}

def normalised_data_fetch(movieid, limit = 10):
    movie_type = list(NormalisedContentbasedfilteringMap.objects.filter(movieid=movieid).values('normalised_key').values())[0]['normalised_key']
    #return list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=movie_type).values())
    similar_movies = list(NormalisedContentbasedfilteringMap.objects.filter(normalised_key=movie_type).exclude(movieid=movieid).values('normalised_key').values())
    #similar_movies = [1]
    if len(similar_movies)<limit:
        similar_types = list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=movie_type).values())[0]
        for i in numeric_values[1:]:
            similar_movies+=list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=similar_types[i]).values())
            if len(similar_movies)>limit:
                break
    similar_movies = [int(i['movieid']) for i in similar_movies]
    return similar_movies

class DataFetcher:
    numeric_values = ['number_0', 'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'number_6', 'number_7',
                      'number_8', 'number_9']

    def movie_title(self, movie_id):
        return formatter.get_from_db(movie_id)['title'].tolist()[0]

    def fetch_SimpleContentbasedfiltering(self,movieid = None):
        info = list(SimpleCollaborativefilteringItemRecommendation.objects.filter(movieid=movieid).values())[0]
        movies_list = []
        for i in numeric_values:
            try:
                movies_list.append(info[i])
            except:
                pass

        return movies_list

    def fetch_SimpleCollaborativefiltering(self, movieid = None, userid=None):

        if userid:

            info =  list(SimpleCollaborativefilteringUserRecommendation.objects.filter(userid=userid).values())[0]
            movies_list = []
            for i in numeric_values:
                try:
                    movies_list.append(info[i])
                except:
                    pass

            return movies_list
        if movieid:
            info =  list(SimpleCollaborativefilteringItemRecommendation.objects.filter(movieid=movieid).values())[0]
            movies_list = []
            for i in numeric_values:
                try:
                    movies_list.append(info[i])
                except:
                    pass

            return movies_list


        return []
    def normalised_data_fetch(movieid, limit = 10):
        movie_type = list(NormalisedContentbasedfilteringMap.objects.filter(movieid=movieid).values('normalised_key').values())[0]['normalised_key']
        #return list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=movie_type).values())
        similar_movies = list(NormalisedContentbasedfilteringMap.objects.filter(normalised_key=movie_type).exclude(movieid=movieid).values('normalised_key').values())
        #similar_movies = [1]
        if len(similar_movies)<limit:
            similar_types = list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=movie_type).values())[0]
            for i in numeric_values[1:]:
                similar_movies+=list(NormalisedContentbasedfilteringSimilarity.objects.filter(movieid=similar_types[i]).values())
                if len(similar_movies)>limit:
                    break
        similar_movies = [int(i['movieid']) for i in similar_movies]
        return similar_movies

#    def fetch_Simple_ContentBasedFiltering(self,id):
