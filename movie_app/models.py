from django.db import models
from django.urls import reverse
from django.utils.text import slugify


'''Создаем модель класса Movie. Для быстрого импорта ALT+ENTER!!!!'''
class Movie(models.Model):
    EURO = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    CURRENCY_CHOICES = [
        (EURO, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Ruble'),
    ]

    name = models.CharField(max_length=40)
    rating = models.IntegerField()
    year = models.IntegerField(null=True)
    budget = models.IntegerField(default=1000000)
    # добавляем выбор валюты из CURRENCY_CHOICES
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)
    # slug параметр для удобного отображения маршрута в браузере, db_index=True ускоряет поиск по БД
    slug = models.SlugField(default='', null=False, db_index=True)


    '''переопределяем метод self для преобразования поля имени (name) с помощью slugify (импортируется выше)'''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    '''Эта функция возвращает функцию reverse от маршрута "movie-details" прописанного в movie_app.urls'''
    def get_url(self):
        return reverse('movie-details', args=[self.slug])   # передаем slug

    '''Эта функция отображает поля, которые будут приходить при запросах all по умолчанию'''
    def __str__(self):
        return f'id {self.id} - {self.name} - {self.rating}% - {self.year}'



# from movie_app.models import Movie - импорт в командную строку для обращения к объектам класса Movie в БД