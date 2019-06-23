from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
# Logics for creating and deletion and in terms of forms

def cover_upload_path(instance, filename):
    return os.path.join('books', instance.seller.username, filename)

class Book(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    orig_price = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    cover_image = models.ImageField(upload_to=cover_upload_path)
    description = models.TextField()
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=10)
    
    def __str__(self):
        return '{}, by {}.'.format(self.title, self.author)
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    add_date = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    add_date = models.DateTimeField(null=True)
    # one of (submitted, completed)
    status = models.CharField(max_length=20)
    # one of (shipping, offline)
    delivery_method = models.CharField(max_length=20)
    
class WishListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    add_date = models.DateTimeField(null=True)
    description = models.TextField()
    
