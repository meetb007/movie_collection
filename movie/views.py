import logging

from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

import shared.request_client as requests

logger = logging.getLogger('django')

movie_api_url = settings.MOVIE_API_URL
movie_api_username = settings.MOVIE_API_USERNAME
movie_api_password = settings.MOVIE_API_PASSWORD
server_url = settings.SERVER_URL


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def fetch_movies(request):
    try:
        page = int(request.GET.get('page', 1))

        url = (movie_api_url + '?page=' + str(page)) if page else movie_api_url
        response = requests.get_with_retry(url)

        data = response.json()
        data['next'] = (server_url + '/movies/?page=' + str(page + 1)) \
            if data['count']//10 >= page+1 else None

        data['previous'] = (server_url + '/movies/?page=' + str(page - 1)) \
            if page > 1 else None
        return Response(data=data, status=200)

    except Exception as e:
        logger.exception(e)
        return Response(
            data={
                'message': 'Something went wrong',
                'exception': str(e)
            },
            status=500
        )
