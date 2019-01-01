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
    path('books_loaned/', views.LoanedBooksListView.as_view(), name='loaned_books')
]
