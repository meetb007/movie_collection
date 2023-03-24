from django.urls import path

from collection.views import CollectionCrudView
from movie.views import fetch_movies

urlpatterns = [
    path('', CollectionCrudView.as_view(),
         name='collection_crud_apis'),
    path('<slug:uuid>/', CollectionCrudView.as_view(),
         name='collection_crud_apis'),
]