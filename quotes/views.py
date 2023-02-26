from django.db.models import Count
from django.views import generic

from .models import Author, Book, Quote


class IndexView(generic.TemplateView):
    template_name = 'quotes/index.html'


class AuthorsView(generic.ListView):
    template_name = 'quotes/authors.html'
    context_object_name = 'entries_list'
    paginate_by = 100
    model = Author

    def get_queryset(self):
        return Author.objects.annotate(Count('book')).annotate(Count('quote')).all()


class QuotesView(generic.ListView):
    template_name = 'quotes/quotes.html'
    context_object_name = 'entries_list'
    paginate_by = 100
    model = Quote

    def get_queryset(self):
        return Quote.objects.select_related('author').prefetch_related('author__book_set')\
            .annotate(Count('author__book')).all()


class BooksView(generic.ListView):
    template_name = 'quotes/books.html'
    context_object_name = 'entries_list'
    paginate_by = 100
    model = Book

    def get_queryset(self):
        return Book.objects.select_related('author').prefetch_related('author__quote_set')\
            .annotate(Count('author__quote')).all()
