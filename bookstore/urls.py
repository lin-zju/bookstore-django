from django.urls import path, include
from .import views
from django_private_chat import urls as django_private_chat_urls

app_name = 'bookstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<username>/', views.profile, name='profile'),
    path('mystore/', views.mystore, name='mystore'),
    path('user_store/<username>/', views.user_store, name='user_store'),
    path('user_wishlist/<username>/', views.user_wishlist, name='user_wishlist'),
    path('mycart/', views.mycart, name='mycart'),
    path('mywishlist/', views.mywishlist, name='mywishlist'),
    path('myorders/', views.myorders, name='myorders'),
    path('received_orders/', views.received_orders, name='received_orders'),
    path('thanks/', views.thanks, name='thanks'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.MyRegistrationView.as_view(), name='register'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/remove/<int:book_id>/', views.remove_book, name='remove_book'),
    path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/do_purchase/<int:cart_id>', views.do_purchase, name='do_purchase'),
    path('cart/confirm_purchase/<int:cart_id>/', views.confirm_purchase, name='confirm_purchase'),
    path('cart/increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('order/complete/<int:order_id>/', views.complete_order, name='complete_order'),
    
    path('', include(django_private_chat_urls)),
    
    path('test/', views.test, name='test')
]
