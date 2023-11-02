from datetime import date

from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    """Category"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actor and Directors"""
    name = models.CharField("Name", max_length=150)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor and Director"
        verbose_name_plural = "Actor and Director"


class Genre(models.Model):
    """Genre"""
    name = models.CharField("Name", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Movie"""
    title = models.CharField("Title", max_length=150)
    subtitle = models.CharField("Subtitle", max_length=150, default='')
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to='movies/')
    year = models.PositiveSmallIntegerField('Release data', default=2023)
    country = models.CharField("Country", max_length=150)
    directors = models.ManyToManyField(Actor, verbose_name='directors', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='actors', related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name='genres')
    world_premiere = models.DateField("World premiere", default=timezone.now)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="Enter the dollar amount")
    fees_in_use = models.PositiveIntegerField(
        "US fees", default=0, help_text="Enter the dollar amount"
    )
    fees_in_world = models.PositiveIntegerField(
        "World fees", default=0, help_text="Enter the dollar amount"
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Category',
        on_delete=models.CASCADE,
    )
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"


class MovieShort(models.Model):
    """Clips form the movies"""
    title = models.CharField("Title", max_length=150)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to='movies_shorts/')
    movie = models.ForeignKey(Movie, verbose_name="Film", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Clips form the movies"
        verbose_name_plural = "Clips form the movies"


class RatingStar(models.Model):
    """Star Rating"""
    value = models.SmallIntegerField("Meaning", default=0)

    def __str__(self):
        return f'{str(self.value)}'

    class Meta:
        verbose_name = "Star Rating"
        verbose_name_plural = "Star Ratings"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=150)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='film')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=150)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey(
        'self',
        verbose_name="Parent",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    movie = models.ForeignKey(Movie, verbose_name='film', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
