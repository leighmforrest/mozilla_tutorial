from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('book/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='user_books'),
    path('books_loaned/', views.LoanedBooksListView.as_view(), name='loaned_books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book'),
    # Author URLs
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    # Book URLs
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]
