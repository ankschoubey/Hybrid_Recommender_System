from django.shortcuts import render
from .models import Ratings
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Count
from .django_data import popularity, ratings_for_movie, normalised_data_fetch
# Create your views here.
from .forms import UserForm, LoginForm
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .data import JSON_formatter
from .core import current_seconds, random_order
from .django_data import insert_update_rating, delete_rating, get_column
from .algorithms import Hybridization


from django.http import HttpResponse
from .django_data import DataFetcher, insert_update_rating, delete_rating
engine = JSON_formatter()

fetcher = DataFetcher()

from .models import Movies

blocked_movies = [170, 266,713,2288,910 ,944 ,1456 ,2039 ,2141 ,3048 ,3104 ,3465 ,4157 ,4464 ,5336 ,6113 ,6963 ,7083 ,7546 ,8633 ,8721 ,8952,3083,3846,7060,4947,5370,6985]

def remove_blocked_movies(movies):
    return movies
    #return [i for i in movies if i not in blocked_movies]

def ajax_update_rating(request):
    if request.method == 'POST':
        userid = request.user.id + 670
        movieid = int(request.POST['movieid'])
        rating = int(request.POST['rating'])
        if rating == 0:
            delete_rating(userid, movieid)
        else:
            insert_update_rating(userid,movieid,rating,current_seconds())

        return HttpResponse('Updated')
    else:
        return HttpResponse('problem')

def ajax_error_loading_image(request):
    if request.method == 'POST':

        # check if image exists in local storage

        # if it does not check get image location and where to save from database
        return HttpResponse('Updated')

    else:
        return HttpResponse('Problem')

class Index(View):

    template_name = 'ui/cards_view.html'

    def get(self, request):
        user_id = None
        movie_id_latest_movie = None
        movie_id_second_movie = None
        cf_user = None
        cf_item = None
        cb_item = None
        svd_cf_user = None
        cvc_hyb_user = None

        hybrid_recommendation = None

        if request.user.id:
            user_id = request.user.id+670
        minimum_rating = 3

        content = {}
        meta = {}

        #insert_update_rating(9123312,1,5,7)
        #delete_rating(9123312,123412)

        # Switching Hybridization
        if user_id:
            try:
                cf_user = fetcher.fetch_SimpleCollaborativefiltering(userid=user_id)
                cf_user = remove_blocked_movies(cf_user)
            except:
                pass

            try:
                svd_cf_user = fetcher.fetch_SvdCollaborativefilteringUserRecommendation(userid=user_id)
                svd_cf_user = remove_blocked_movies(svd_cf_user)
            except:
                print('Fetched Value',fetcher.fetch_SvdCollaborativefilteringUserRecommendation(userid=user_id))
                pass

            try:
                cvc_hyb_user = fetcher.fetch_CollaborativeViaContentUserRecommendation(userid=user_id)
                cvc_hyb_user = remove_blocked_movies(cvc_hyb_user)
            except:
                print('Fetched Value',fetcher.fetch_CollaborativeViaContentUserRecommendation(userid=user_id))

                pass
            try:
                movies = list(Ratings.objects.filter(userid = user_id, rating__gte=minimum_rating).order_by('-timestamp').values('movieid'))
                movie_id_latest_movie = movies[0]['movieid']
                movie_id_second_movie = movies[1]['movieid']
            except:
                pass

            if movie_id_latest_movie:
                cf_item = fetcher.fetch_SimpleCollaborativefiltering(movieid=movie_id_latest_movie)
                cf_item = remove_blocked_movies(cf_item)

            if movie_id_second_movie:
                cb_item = fetcher.fetch_SimpleContentbasedfiltering(movieid=movie_id_second_movie)
                cb_item = remove_blocked_movies(cb_item)

        recommendations_not_null = [i for i in [cf_user, svd_cf_user, cvc_hyb_user, cf_item, cb_item] if i]

        if len(recommendations_not_null)>1:
            hybrid_recommendation = Hybridization.mixed(recommendations_not_null)[:10]
            #hybrid_recommendation = random_order(hybrid_recommendation)

        if hybrid_recommendation:
            key = 'Recommended for you'
            content[key] = hybrid_recommendation
            meta[key] = {'subheading': 'Mixed Hybridization'}

        if cf_user:
            key = 'Based on users similar to you'
            content[key] = cf_user
            meta[key] = {'subheading': 'User Based Collaborative Filtering'}

        if svd_cf_user:
            key = 'Another way of finding similar users'
            content[key] = svd_cf_user
            meta[key] = {'subheading': 'Collaborative Filtering using SVD'}

        if cvc_hyb_user:
            key = 'Collaborative Via Content Based'
            content[key] = cvc_hyb_user
            meta[key] = {'subheading': 'Feature Combination Hybridization'}

        if cf_item:
            key = 'People who watched ' + fetcher.movie_title(movie_id=movie_id_latest_movie) + ' also watched this:'
            content[key] = cf_item
            meta[key] = {'subheading': 'Item Based Collaborative Filtering'}

        if cb_item:
            key = 'Based on ' + fetcher.movie_title(movie_id=movie_id_second_movie)

            content[key] = cb_item
            meta[key] = {'subheading': 'Content Based Filtering'}

        # start creating content to displat

        # if user_id:
        #
        #     try:
        #         content['Based on users similar to you'] = fetcher.fetch_SimpleCollaborativefiltering(userid=user_id)
        #         meta['Based on users similar to you'] = {'subheading': 'User Based Collaborative Filtering'}
        #     except:
        #         pass
        #
        #     try:
        #         movies = list(Ratings.objects.filter(userid = user_id, rating__gte=minimum_rating).order_by('-timestamp').values('movieid'))
        #         movie_id_latest_movie = movies[0]['movieid']
        #         movie_id_second_movie = movies[1]['movieid']
        #         print('movie_id_latest_movie',movie_id_latest_movie)
        #         print('movie_id_latest_movie',movie_id_second_movie)
        #
        #         print('name ', fetcher.movie_title(movie_id=movie_id_latest_movie))
        #
        #         if not movie_id_latest_movie:
        #             raise Exception('Movie Id Latest Not Present')
        #
        #         key = 'People who watched ' + fetcher.movie_title(
        #             movie_id=movie_id_latest_movie) + ' also watched this:'
        #         print(key)
        #         content[key] = fetcher.fetch_SimpleCollaborativefiltering(movieid=movie_id_latest_movie)
        #
        #         meta[key] = {'subheading': 'Item Based Collaborative Filtering'}
        #
        #     except Exception as e:
        #         print('error',e)
        #
        #         pass
        #
        #     try:
        #         #print('movie_id_second_movie',movie_id_second_movie)
        #         #print('contentbased',fetcher.fetch_SimpleContentbasedfiltering(
        #         #    movieid=movie_id_second_movie))
        #         #print('moviename ',fetcher.movie_title(movie_id=movie_id_second_movie))
        #         if not movie_id_second_movie:
        #             raise Exception('Movie Id Latest Not Present')
        #         key = 'Based on ' + fetcher.movie_title(movie_id=movie_id_second_movie)
        #
        #         content[key] = fetcher.fetch_SimpleContentbasedfiltering(
        #             movieid=movie_id_second_movie)
        #         meta[key] = {'subheading': 'Content Based Filtering'}
        #     except:
        #         pass

        content['Most Popular Movies'] = remove_blocked_movies(fetcher.fetch_Popularitybasedfiltering())
        meta['Most Popular Movies'] = {'subheading': 'Popularity Based Filtering'}



        #content['Most Popular']=popularity()

        #return HttpResponse(str(content)+'123')

        #content['Action'] = [5,6,4,3,2,1,2,4,4,3]#/popularity()

        data = engine.format(content)
        #return HttpResponse(str(data)+'123')
        data['meta']=meta

        return render(request, self.template_name, data)

class MovieView(View):
    template_name = 'ui/movie_details.html'

    def get(self, request, pk):
        movieid = int(pk)

        temp_response = {}

        response = {}
        meta = {}
        response['detailed_movie'] = engine.format({'a':[movieid]})['movies'][movieid]
        response['detailed_movie']['id'] = movieid

        #return HttpResponse(str(normalised_data_fetch(pk)))

        movies_with_similar_name = fetcher.fetch_BagOfWordsContentbasedfilteringRecommend(movieid=pk)
        if movies_with_similar_name:
            movies_with_similar_name = list(movies_with_similar_name)
            key = 'Movies with similar names'
            temp_response[key] = movies_with_similar_name
            meta[key] = {'subheading': 'Bag of Words Content Based Filtering'}
            #return HttpResponse(str(movies_with_similar_name) + ' ' +str(type(movies_with_similar_name)))

        similar_movies = remove_blocked_movies(normalised_data_fetch(movieid))[:10]
        key = 'Similar Movies'
        temp_response[key] = similar_movies

        user_who_like_this_also_liked = remove_blocked_movies(fetcher.fetch_SimpleCollaborativefiltering(movieid=movieid))[:10]
        key = 'User who watched this also watched'
        temp_response[key] = user_who_like_this_also_liked

        data = engine.format(temp_response)

        meta['Similar Movies'] = {'subheading': 'Normalised Content Based Filtering'}
        meta['User who watched this also watched'] = {'subheading': 'Item based Collaborative Filtering'}

        response['content'] = temp_response
        response['movies'] = data['movies']
        response['meta']=meta
        return render(request, self.template_name, response)
        #return HttpResponse(str(response))

    #
    # def get(self, request, pk):
    #     pk = int(pk)
    #     response = {}
    #     meta = {}
    #     response['detailed_movie'] = engine.format({'a':[pk]})['movies'][pk]
    #     response['detailed_movie']['id'] = pk
    #     #return HttpResponse(str(normalised_data_fetch(pk)))
    #
    #     similar_movies = remove_blocked_movies(normalised_data_fetch(pk))[:10]
    #     user_who_like_this_also_liked = remove_blocked_movies(fetcher.fetch_SimpleCollaborativefiltering(movieid=pk))[:10]
    #
    #     movies_with_similar_name = list(fetcher.fetch_BagOfWordsContentbasedfilteringRecommend(movieid=pk))
    #
    #     temp = {}
    #
    #     # if movies_with_similar_name:
    #     #     temp['Movies with similar names'] = movies_with_similar_name
    #     #     return HttpResponse('Movies with similar names'+str(movies_with_similar_name)+str(type(movies_with_similar_name)))
    #     #
    #     #     meta['Movies with similar names'] = {'subheading': 'Content Based Filtering using Bag of Words'}
    #     temp['Similar Movies'] = similar_movies
    #     temp['Users who liked this also liked'] = user_who_like_this_also_liked
    #
    #     data = engine.format(temp)
    #
    #     meta['Similar Movies'] = {'subheading': 'Normalised Content Based Filtering'}
    #     meta['User who watched this also watched'] = {'subheading': 'Item based Collaborative Filtering'}
    #
    #     response['content'] = temp
    #     response['movies'] = data['movies']
    #     response['meta']=meta
    #     return HttpResponse(str(response))
    #
    #     #return render(request, self.template_name, response)
    #     #return HttpResponse(str(response))


class UserFormView(View):
    form_class = UserForm
    # what is the blueprint that you are going to use for form

    template_name = 'ui/register.html'

    # in class based views, you can take you get and post logic and seperate it into built in functions

    def get(self, request):
        form = self.form_class(None)# by default it has no data
        return render(request, self.template_name, {'form': form})

        pass

    def post(self, request):
        form = self.form_class(request.POST)# all data gets stored in POST

        if form.is_valid():
            # take information and store in database

            # before that make checks

            user = form.save(commit=False)
            # create object from form but saved it locally

            # clean/secure data
            # ready to enter database

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    request.user.userid  = 670+user.id
                    print('user id is ',request.user.userid)
                    return redirect('ui:index')

        return render(request, self.template_name, {'form': form})

class LoginFormView(View):
    form_class = UserForm
    # what is the blueprint that you are going to use for form

    template_name = 'ui/login.html'

    # in class based views, you can take you get and post logic and seperate it into built in functions

    def get(self, request):
        form = self.form_class(None)# by default it has no data
        return render(request, self.template_name, {'form': form})

        pass

    def post(self, request):
        form = self.form_class(request.POST)# all data gets stored in POST
        username = request.POST.get('username')
        password = request.POST.get('password')#]#('payment_id', '')
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            request.user.userid = 670+user.id
            return redirect('ui:index')
        except:
            return render(request, self.template_name, {'form': form})

        if form.is_valid():
            # take information and store in database

            # before that make checks
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username = username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    request.user.userid  = 670+user.id
                    # request.user.username  = session info

                    return redirect('ui:index')


from django.views import generic

class Search(generic.ListView):
    template_name = 'ui/search.html'
    model = Movies

    #context_object_name = 'movies'
    # default is object_list

    def post(self, request, *args, **kwargs):
        search_term = request.POST.get('search_term')
        stuff = self.get_queryset().filter(title__icontains=search_term)
        print(stuff.values())
        return render(request, self.template_name, {'object_list': stuff, 'search_term': search_term})

    def get_queryset(self):

        try:
            name = self.kwargs['name']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(title__icontains = name)
        else:
            object_list = self.model.objects.all()
        return object_list

class ProfileView(generic.View):
    template_name = 'ui/profile.html'
    model = Ratings

    def get(self, request):
        user_id = request.user.id + 670
        data = {}



        all_info =  list(Ratings.objects.filter(userid=user_id).order_by('-timestamp').values_list('movieid', 'rating'))
        #movie_ids = get_column(all_info,0)

        content = []
        for i, j in all_info:
            temp = {'movieid': i}
            object_list = list(Movies.objects.filter(movieid=i).values())[0]
            temp['title']=object_list['title']
            temp['year']=object_list['year']
            temp['rating']=j
            content.append(temp)

       # data['movies'] = JSON_formatter().format({'rated_movies':movie_ids})['movies']
        data['user_profile'] = fetcher.fetch_CollaborativeViaContentUserprofile(user_id)

        #return HttpResponse(str(data['user_profile']))

        data['user_history'] = content

        return render(request, self.template_name,data)