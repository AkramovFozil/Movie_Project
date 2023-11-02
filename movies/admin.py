from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

from .models import Movie, MovieShort, Actor, Genre, RatingStar, Rating, Category, Reviews
from django import forms


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Categories"""
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('email', 'name')


class MovieShortsInline(admin.TabularInline):
    model = MovieShort
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200" height="100"')

    get_image.short_description = "Image"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Movies"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year',)
    search_fields = ('title', 'category__name',)
    inlines = [ReviewInline, MovieShortsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            "fields": (("title", "subtitle"),)
        }),
        (None, {
            "fields": (("description", "poster", 'get_image'),)
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ('collapse',),
            "fields": (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            "fields": (('budget', 'fees_in_use', 'fees_in_world'),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),

    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="auto"')

    get_image.short_description = "Image"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Reviews"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Actors"""
    list_display = ("name", "age", 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating"""
    list_display = ("star", "movie", 'ip')


@admin.register(MovieShort)
class MovieShortAdmin(admin.ModelAdmin):
    """MovieShorts"""
    list_display = ("title", "movie", 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200" height="100"')

    get_image.short_description = "Image"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
