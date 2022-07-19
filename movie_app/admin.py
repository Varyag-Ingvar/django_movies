from django.contrib import admin

# Register your models here.
from movie_app.models import Movie
from django.db.models import QuerySet

'''создаем свой фильтр для админки'''
class RatingFilter(admin.SimpleListFilter):
    title = 'Rating filter'      # обязательно прописываем эти 2 параметра!!!
    parameter_name = 'rating_set'

    def lookups(self, request, model_admin):  # задаем названия нужных нам критериев фильтрации
        return [
            ('<40', 'low'),
            ('40 to 59', 'medium'),
            ('60 to 79', 'hi'),
            ('>=80', 'top')
        ]

    def queryset(self, request, queryset: QuerySet):  # прописываем логику фильтрации
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)     # достаем из queryset значение рейтинга и фильтруем его
        if self.value() == '40 to 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == '60 to 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        return queryset




@admin.register(Movie)  # регистрируем нашу модель Movie с помощью декоратора, для доступа к ней из админ-панели
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rating', 'currency', 'budget', 'rating_status']  # тут прописываем поля, которые хотим видеть в админке
    list_editable = ['name', 'rating', 'currency', 'budget']  # создаем список полей, которые можно редактировать
    # list_per_page = 5    # можем задавать пагинацию, сколько строк будет отображаться на странице админки
    # ordering = ['name']  # сортировка по определенным полям
    actions = ['set_dollars', 'set_euro']  # регистрируем методы set_dollars и set_euro в админке
    search_fields = ['name']  # создаем возможность поиска по нужным полям
    list_filter = ['name', 'currency', RatingFilter]  # создаем панель фильтрации нужных нам полей

    '''задаем новое поле, в котором пишем какую-либо логику, в данном случае присвоение 'смотрибельности' по рейтингу'''
    @admin.display(ordering='rating')  # позволяет сортировать поле по другому полю, в данном случае по рейтингу
    def rating_status(self, movie: Movie):
        if movie.rating < 50:
            return 'Trash!'
        if movie.rating < 70:
            return 'Can see it once'
        if movie.rating <= 80:
            return 'Cool movie!'
        return 'Top class movie!'


    '''в этом методе задаем валюту, которую сможем применять в админке к выбранным строкам'''
    @admin.action(description='установить валюту доллар')
    def set_dollars(self, request, queryset: QuerySet):
        queryset.update(currency=Movie.USD)

    @admin.action(description='установить валюту евро')
    def set_euro(self, request, queryset: QuerySet):
        count_updated = queryset.update(currency=Movie.EURO)
        self.message_user(    # выводит сообщение при применении метода по смене валюты
            request,
            f'{count_updated} entries updated!'
        )



