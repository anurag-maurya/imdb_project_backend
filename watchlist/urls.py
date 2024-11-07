from django.urls import path
from .views import movies_list, movie_details
urlpatterns = [
    path('list/', movies_list, name="movies_list"),
    path('<int:pk>/', movie_details, name="movie_details"),
]
