from django import forms
from django.forms import ModelForm
from .models import *

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        

class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

class WishListItem(ModelForm):
    class Meta:
        model = WishListItem
        fields = '__all__'
    
