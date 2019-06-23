from django.urls import path, include
from .import views

app_name = 'bookstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('mystore/', views.mystore, name='mystore'),
    path('thanks/', views.thanks, name='thanks'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('book/add', views.add_book, name='add_book'),
    path('book/edit/<int:book_id>', views.edit_book, name='edit_book'),
]
