from . import views
from django.urls import path

# создаем пути(маршруты) для приложения movie_app
urlpatterns = [
    path('', views.show_all_movies),
    path('movie/<slug:slug_movie>', views.show_one_movie, name='movie-details'),  # передаем конвертер slug в маршрут!
]