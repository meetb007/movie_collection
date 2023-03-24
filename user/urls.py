from django.urls import path

from user.views import create_user, login_user

urlpatterns = [
    path('', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
]
