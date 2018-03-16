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
from .core import current_seconds
from .django_data import insert_update_rating, delete_rating


from django.http import HttpResponse
from .django_data import DataFetcher, insert_update_rating, delete_rating
engine = JSON_formatter()

fetcher = DataFetcher()

from .models import Movies


def ajax_update_rating(request):
    if request.method == 'POST':
        userid = 999999 ###UserId
        movieid = int(request.POST['movieid'])
        rating = int(request.POST['rating'])
        if rating == 0:
            delete_rating(userid, movieid)
        else:
            insert_update_rating(userid,movieid,rating,current_seconds())

        return HttpResponse('Updated')
    else:
        return HttpResponse('problem')

class Index(View):

    template_name = 'ui/cards_view.html'

    def get(self, request):
        user_id = 2
        minimum_rating = 3
        content = {}
        movie_id_latest_movie = None
        movie_id_second_movie = None
        #insert_update_rating(9123312,1,5,7)
        #delete_rating(9123312,123412)

        try:
            content['Recommended for you'] = fetcher.fetch_SimpleCollaborativefiltering(userid=user_id)
        except:
            pass
        content['Most Popular Movies'] = fetcher.fetch_Popularitybasedfiltering()


        try:
            movies = list(Ratings.objects.filter(userid = user_id, rating__gte=minimum_rating).order_by('-timestamp').values('movieid'))
            movie_id_latest_movie = movies[0]['movieid']
            movie_id_second_movie = movies[1]['movieid']
            print('movie_id_latest_movie',movie_id_latest_movie)
            print('name ', fetcher.movie_title(movie_id=movie_id_latest_movie))
            content['People who watched ' + fetcher.movie_title(
                movie_id=movie_id_latest_movie) + ' also watched this:'] = fetcher.fetch_SimpleCollaborativefiltering(movieid=1)
        except Exception as e:
            print(e)

            pass

        try:
            #print('movie_id_second_movie',movie_id_second_movie)
            #print('contentbased',fetcher.fetch_SimpleContentbasedfiltering(
            #    movieid=movie_id_second_movie))
            #print('moviename ',fetcher.movie_title(movie_id=movie_id_second_movie))
            content['Based on ' + fetcher.movie_title(movie_id=movie_id_second_movie)] = fetcher.fetch_SimpleContentbasedfiltering(
                movieid=movie_id_second_movie)
        except:
            pass

        #content['Most Popular']=popularity()

        #return HttpResponse(str(content)+'123')

        #content['Action'] = [5,6,4,3,2,1,2,4,4,3]#/popularity()

        data = engine.format(content)
        #return HttpResponse(str(data)+'123')

        return render(request, self.template_name, data)

class MovieView(View):
    template_name = 'ui/movie_details.html'

    def get(self, request, pk):
        pk = int(pk)
        response = {}

        response['detailed_movie'] = engine.format({'a':[pk]})['movies'][pk]
        response['detailed_movie']['id'] = pk
        #return HttpResponse(str(normalised_data_fetch(pk)))

        similar_movies = normalised_data_fetch(pk)[:5]
        user_who_like_this_also_liked = fetcher.fetch_SimpleCollaborativefiltering(movieid=pk)[:5]

        data = engine.format({'Similar Movies':similar_movies,'Users who liked this also liked':user_who_like_this_also_liked})
        response['similar_movies'] = similar_movies
        response['user_who_like'] = user_who_like_this_also_liked
        response['content'] = {'Similar Movies': similar_movies,'User who watched this also watched': user_who_like_this_also_liked}
        response['movies'] = data['movies']
        return render(request, self.template_name, response)
        #return HttpResponse(str(response))




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
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']


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

        return render(request, self.template_name, {'form': form})

from django.views import generic

class Search(generic.ListView):
    template_name = 'ui/search.html'
    model = Movies

    #context_object_name = 'movies'
    # default is object_list

    def post(self, request, *args, **kwargs):
        search_term = request.POST.get('search_term')
        stuff = self.get_queryset().filter(title__icontains=search_term)
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