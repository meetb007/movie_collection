import uuid

from django.db import transaction
from rest_framework.response import Response

from movie.forms.movie_forms import MovieForm
from movie.models import Movie
from movie.view_utils.genre_helper import bulk_create_genres


@transaction.atomic()
def bulk_create_movies(movie_list):

    movie_id_list = []

    for movie in movie_list:
        movie_form = MovieForm(movie)

        if not movie_form.is_valid():
            return False, Response(
                data={
                    'message': movie_form.errors
                },
                status=400
            ), None

        movie_data = movie_form.cleaned_data

        movie_id_list.append(movie_data['uuid'])
        movie['id'] = movie.pop('uuid')

    movie_obj_list = Movie.objects\
        .filter(id__in=movie_id_list)

    existing_movie_id_list = movie_obj_list\
        .values_list('id', flat=True)

    for movie in movie_list:

        if uuid.UUID(movie['id']) not in existing_movie_id_list:

            genres = movie.pop('genres')
            movie_obj = Movie.objects.create(**movie)
            list(movie_obj_list).append(movie_obj)

            if genres:
                genre_name_list = genres.split(',')
                genres = bulk_create_genres(genre_name_list)
                movie_obj.genre.set(genres)

    return True, None, movie_obj_list
