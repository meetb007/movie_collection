from django.urls import path

from request_counter.views import fetch_request_counter, reset_request_counter

urlpatterns = [
    path('', fetch_request_counter, name='fetch_request_counter'),
    path('reset/', reset_request_counter, name='reset_request_counter')
]
