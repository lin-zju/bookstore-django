from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

# Create your models here.
# Logics for creating and deletion and in terms of forms

def cover_upload_path(instance, filename):
    return os.path.join('books', instance.seller.username, filename)

class Book(models.Model):
    
    # category choices
    COMPUTER = 'COM'
    MATH = 'MATH'
    PHYSICS = 'PHYSICS'
    OTHER = 'OTHER'
    CATEGORY_CHOICES = [
        (COMPUTER, 'computer'),
        (MATH, 'math'),
        (PHYSICS, 'physics'),
        (OTHER, 'other')
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    orig_price = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    cover_image = models.ImageField(upload_to=cover_upload_path)
    description = models.TextField(default='no description')
    
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    isbn = models.CharField(max_length=13)
    
    def __str__(self):
        return '{}, by {}.'.format(self.title, self.author)
    
    def get_link_to_douban(self):
        return 'http://douban.com/isbn/{}/'.format(self.isbn)
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    date_added = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return "Title: {title}, Date: {date}, Quantity: {quantity}".format(
            title=str(self.book.title),
            date=datetime.now().strftime('%Y-%m-%d'),
            quantity=self.quantity
        )
    
class OrderItem(models.Model):
    # status choices
    PROCESSING = 'PR'
    COMPLETED = 'CO'
    STATUS_CHOICES = [
        (PROCESSING, 'processing'),
        (COMPLETED, 'completed')
    ]
    # delivery methods
    SHIPPING = 'SH'
    OFFLINE = 'OF'
    DELIVERY_CHOICES = [
        (SHIPPING, 'shipping'),
        (OFFLINE, 'offline')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    
    def __str__(self):
        return 'Title: {}, Quantity: {}, Status: {}, Delivery method: {}'.format(
            self.book.title,
            self.quantity,
            self.get_status_display(),
            self.get_delivery_method_display()
        )
    
    def is_completed(self):
        return self.status == self.COMPLETED
    
class WishListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(null=True)
    description = models.TextField(default='no description')
    
    def __str__(self):
        return "Title: {title}, Date: {date}".format(
            title=str(self.book.title),
            date=datetime.now().strftime('%Y-%m-%d'),
        )
    
