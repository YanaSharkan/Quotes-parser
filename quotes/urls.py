from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import path
from django.views.decorators.cache import cache_page


from . import views

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


app_name = 'quotes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('authors/', cache_page(CACHE_TTL)(views.AuthorsView.as_view()), name='authors'),
    path('books/', cache_page(CACHE_TTL)(views.BooksView.as_view()), name='books'),
    path('quotes/', cache_page(CACHE_TTL)(views.QuotesView.as_view()), name='quotes'),
]
