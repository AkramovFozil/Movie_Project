from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=2):
    movies = Movie.objects.order_by('id')[:count]
    context = {
        'last_movies': movies,
    }
    return context
