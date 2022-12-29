from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField('категория', max_length=100)
    description = models.TextField()
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Actor(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='actors/')
     
    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = 'актеры и режиссер'
        verbose_name_plural = 'актеры и режиссеры'


class  Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.SlugField(max_length=150, unique=True)
        

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Movie(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to='movies/')
    year = models.PositiveSmallIntegerField(default=0)
    country = models.CharField(max_length=100)
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актеры', related_name='filn_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull = True)
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из Фильма'
                
class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    ip = models.CharField(max_length=100)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинга'



class Reviews(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=100)
    text = models.TextField()
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'