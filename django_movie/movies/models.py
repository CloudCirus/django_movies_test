from django.db import models
from datetime import date


class Category(models.Model):
    """Категория фильмов"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        # verbose_name_pr = 'Категории'


class Actor(models.Model):
    """Актеры и режисcеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveIntegerField('Возраст', default=0)
    description = models.TextField('описание')
    image = models.ImageField('Изображение', upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер и режисcер'
        # verbose_name_pr = 'Актеры и режисcеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        # verbose_name_pr = 'Жанры'


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField('Название', max_length=100)
    tegline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.SmallIntegerField('Дата выхода', default=2019)
    country = models.CharField('Страна производства', max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актер', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанр')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Укажите бюджет в долларах')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='Укажите сумму в долларах')
    fees_in_world = models.PositiveIntegerField('Сборы в США', default=0, help_text='Укажите сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        # verbose_name_pr = 'Фильмы'


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movies_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        # verbose_name_pr = 'Кадры из фильмов'


class RatingStars(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        # verbose_name_pr = 'Звезды рейтинга'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        # verbose_name_pr = 'Рейтинги'


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        # verbose_name_pr = 'Отзывы'
