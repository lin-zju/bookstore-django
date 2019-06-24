from django import forms
from django.forms import ModelForm
from .models import *

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['seller']
        

class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderItemForm(ModelForm):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField(default=1)
    # date_added = models.DateTimeField(null=True)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    class Meta:
        model = OrderItem
        fields = ['delivery_method']

class WishListItemForm(ModelForm):
    class Meta:
        model = WishListItem
        fields = '__all__'
        
    
