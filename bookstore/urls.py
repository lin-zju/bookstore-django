from django.urls import path, include
from .import views

app_name = 'bookstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('thanks/', views.thanks, name='thanks'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('book/add', views.add_book, name='add_book'),
]
