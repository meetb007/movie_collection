
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def fetch_request_counter(request):
    counter = cache.get('request_counter', 0)
    return Response({"requests": counter})


@api_view(['POST'])
def reset_request_counter(request):
    cache.set('request_counter', 0)
    return Response({"message": "request count reset successfully"})
