from django.conf.urls import url
from .import views
from django.contrib.auth.views import logout

app_name ='ui'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login$', views.LoginFormView.as_view(), name='login'),
    url(r'^(?P<pk>[0-9]+)/$', views.MovieView.as_view()),
    url(r'update_rating', views.ajax_update_rating),
    url(r'search', views.Search.as_view()),
]