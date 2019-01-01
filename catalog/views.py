from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre


class HomePageView(generic.TemplateView):
    """View class for home page of site."""
    template_name = 'catalog/index.html'

    def get_context_data(self):
        # Number of visits to this view, as counted in the session
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        print(num_visits)
        # Generate counts of some of the main objects
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()

        # Available books (status = 'a')
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()

        # The 'all()' is implied by default
        num_authors = Author.objects.count()

        genre_books = Book.objects.filter(genre__name__icontains='fiction').count()
        print(genre_books)

        sea_books = Book.objects.filter(title__icontains='sea').count()

        context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'genre_books': genre_books,
            'sea_books': sea_books,
            'num_visits': num_visits
        }
        return context


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'catalog/book_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.all()
        # return Book.objects.filter(title__icontains='sea')


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'catalog/author_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/user_books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/loaned_books.html'
    context_object_name = 'books'
    paginate_by = 3
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
