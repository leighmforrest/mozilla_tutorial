import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# FBV imports
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.urls import reverse, reverse_lazy


from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


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
    paginate_by = 10

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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by Librarian."""

    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:loaned_books'))

    # I this is a GET, create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renewal.html', context)

    book_instance = get_object_or_404(BookInstance)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016'}
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/author_form.html'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    template_name = 'catalog/author_delete.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'catalog/book_form.html'
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'catalog/book_delete.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:authors')
