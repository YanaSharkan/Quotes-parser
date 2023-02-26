from django.contrib import admin

from .models import Author, Quote, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'about', 'born', 'location')


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('body', 'author')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pages')
