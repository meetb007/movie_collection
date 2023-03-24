from django.core.cache import cache


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        counter = cache.get('request_counter', 0)
        cache.set('request_counter', counter + 1)
        response = self.get_response(request)
        return response
