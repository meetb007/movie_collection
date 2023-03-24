import logging

from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from collection.forms.collection_forms import CollectionForm, \
    CollectionUpdationForm
from collection.models import Collection
from collection.serializers.collection_serializer import CollectionSerializer
from collection.view_utils.genre_helper import fetch_favourite_genres
from collection.view_utils.movie_helper import fetch_movie_details
from collection.view_utils.user_authentication_helper import validate_user
from movie.view_utils.movie_helper import bulk_create_movies

logger = logging.getLogger('django')


class CollectionCrudView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid=None):
        try:
            is_valid_user, response, user = validate_user(request)

            if not is_valid_user:
                return response

            if uuid:
                response = Collection.objects\
                    .filter(user=user, id=uuid)\
                    .values('title', 'description').first()

                response['movies'] = fetch_movie_details(user=user, uuid=uuid)
            else:
                collection_data = Collection.objects.filter(user=user)

                collection_data = CollectionSerializer(collection_data,
                                                       many=True).data

                response = {
                    "is_success": True,
                    "data": {
                        "collections": collection_data
                    },
                    "favourite_genres": fetch_favourite_genres(user)
                }

            return Response(data=response, status=200)

        except Exception as e:
            logger.exception(e)
            return Response(
                data={
                    'message': 'Something went wrong',
                    'exception': str(e)
                },
                status=500
            )

    def post(self, request):
        try:
            is_valid_user, response, user = validate_user(request)

            if not is_valid_user:
                return response

            collection_form = CollectionForm(request.data)

            if not collection_form.is_valid():
                return Response(
                            data={
                                'message': collection_form.errors
                            },
                            status=400
                        )

            collection_data = collection_form.cleaned_data

            movie_list = collection_data.pop('movies')

            with transaction.atomic():

                is_movies_valid, response, movies_obj_list = \
                    bulk_create_movies(movie_list)

                if not is_movies_valid:
                    return response

                collection_obj = Collection.objects\
                    .create(**collection_data, user=user)

                collection_obj.movie.set(movies_obj_list)

            response = {
                "collection_uuid": collection_obj.id
            }

            return Response(data=response, status=201)

        except Exception as e:
            logger.exception(e)
            return Response(
                data={
                    'message': 'Something went wrong',
                    'exception': str(e)
                },
                status=500
            )

    def put(self, request, uuid=None):
        try:
            is_valid_user, response, user = validate_user(request)

            if not is_valid_user:
                return response

            if not uuid:
                return Response(
                    data={
                        'message': 'Please enter the collection uuid.'
                    },
                    status=400
                )

            collection_form = CollectionUpdationForm(request.data)

            if not collection_form.is_valid():
                return Response(
                            data={
                                'message': collection_form.errors
                            },
                            status=400
                        )

            collection_data = collection_form.cleaned_data
            collection_data = {k: v for k, v in collection_data.items()
                               if v}

            movie_list = None
            if collection_data.get('movies'):
                movie_list = collection_data.pop('movies')

            with transaction.atomic():

                collection_obj = Collection.objects \
                    .filter(user=user, id=uuid)

                collection_obj\
                    .update(**collection_data)

                if movie_list:
                    is_movies_valid, response, movies_obj_list = \
                        bulk_create_movies(movie_list)

                    if not is_movies_valid:
                        return response

                    collection_obj.first().movie.set(movies_obj_list)

            return Response(data={
                'message': 'Collection updated successfully.'
            }, status=200)

        except Exception as e:
            logger.exception(e)
            return Response(
                data={
                    'message': 'Something went wrong',
                    'exception': str(e)
                },
                status=500
            )

    def delete(self, request, uuid=None):
        is_valid_user, response, user = validate_user(request)

        if not is_valid_user:
            return response

        if not uuid:
            return Response(
                data={
                    'message': 'Please enter the collection uuid.'
                },
                status=400
            )

        collection_obj = Collection.objects \
            .filter(user=user, id=uuid)
        collection_obj.delete()

        return Response(data={
            'message': 'Collection deleted successfully.'
        }, status=200)

