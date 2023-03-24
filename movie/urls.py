from django.urls import path

from movie.views import fetch_movies

urlpatterns = [
    path('', fetch_movies,
         name='fetch_movies_from_third_party_api'),
]