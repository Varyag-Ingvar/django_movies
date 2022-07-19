from django.shortcuts import render, get_object_or_404
from movie_app.models import Movie
from django.db.models import Value, F, Sum, Max, Min, Count, Avg  # импорт функций для аггрегации данных из БД


'''выводим список всех фильмов в шаблоне all_movies.html'''
def show_all_movies(request):
    # movies = Movie.objects.all()  выводит все строки из таблицы БД
    movies = Movie.objects.order_by('name')  # сортирует по алфавиту поля name (можно сортировать по любому полю модели)
    # movies = Movie.objects.annotate(   # можем создавать доп.колонки, работать с ними, но в БД они не сохраняются
    #     bool_field=Value(True),
    #     str_field=Value('moviezz'),
    #     int_field=Value(777),
    #     new_budget=F('budget')+100,
    # )
    '''аггрегируем данные с функцией aggregate - выводить будем средний бюджет, максимальный и минимальный рейтинги'''
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'))
    '''c помощью этого цикла проставили поле slug всем элементам в БД, затем закомментировали цикл за ненадобностью'''
    # for movie in movies:
    #     movie.save()

    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg,  # добавляем в контекст вывод аггрегации
        'total': movies.count()  # считаем общ.кол-во фильмов в БД
    })


'''выводим один фильм по id в шаблоне one_movie.html'''
def show_one_movie(request, slug_movie:str):
    movie = get_object_or_404(Movie, slug=slug_movie)   # будет искать фильм по полю slug
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })

