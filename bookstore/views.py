from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
import datetime

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        booklist = Book.objects.all()
        return render(request, 'bookstore/index.html', {'booklist': booklist})
    else:
        return redirect('bookstore:login')
    
@login_required
def mystore(request):
    booklist = Book.objects.filter(seller=request.user)
    return render(request, 'bookstore/mystore.html', {'booklist': booklist})
    
@login_required
def mycart(request):
    cartlist = CartItem.objects.filter(user=request.user)
    return render(request, 'bookstore/mycart.html', {'cartlist': cartlist})

@login_required
def mywishlist(request):
    wishlist = WishListItem.objects.filter(user=request.user)
    return render(request, 'bookstore/mywishlist.html', {'wishlist': wishlist})
    

def thanks(request):
    return HttpResponse('<h1>Thanks!</h1>')

class MyLoginView(auth_views.LoginView):
    # pass
    extra_context = {
        'next': lambda: reverse('bookstore:index')
    }
    
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bookstore:add_book')
    else:
        form = BookForm()
        
    return render(request, 'bookstore/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookstore:edit_book', book.id)
    else:
        form = BookForm(instance=book)
    
    return render(
        request,
        'bookstore/edit_book.html',
        {'form': form, 'pk': book.pk})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        # check whether the book already exists, otherwise create it
        (cart_item, created) = CartItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={
                'date_added': datetime.datetime.now(),
                'quantity': 1
            }
        )
        if not created:
            # already exists
            cart_item.quantity += 1
            cart_item.save()
        return redirect('bookstore:index')
    else:
        raise Http404('Invalid method "{}"'.format(request.method))

@login_required
def remove_from_cart(request, cart_id):
    if request.method == 'POST':
        # check whether the book already exists, otherwise create it
        cartlist = CartItem.objects.filter(id=cart_id)
        cartlist.delete()
        return redirect('bookstore:mycart')
    else:
        raise Http404('Invalid method "{}"'.format(request.method))
    
@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        # check whether the book already exists, otherwise create it
        (cart_item, created) = WishListItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={
                'date_added': datetime.datetime.now(),
            }
        )
        return redirect('bookstore:index')
    else:
        raise Http404('Invalid method "{}"'.format(request.method))

@login_required
def remove_from_wishlist(request, wishlist_id):
    if request.method == 'POST':
        # check whether the book already exists, otherwise create it
        wishlist = WishListItem.objects.filter(id=wishlist_id)
        wishlist.delete()
        return redirect('bookstore:mywishlist')
    else:
        raise Http404('Invalid method "{}"'.format(request.method))
    
@login_required
def confirm_purchase(request, cart_id):
    cart_item = get_object_or_404(CartItem, pk=cart_id)
    order_fields = [
        ('Book title', cart_item.book.title),
        ('Quantity', cart_item.quantity),
    ]
    
    # order = OrderItem.objects.create(**order_fields)
    
    form = OrderItemForm()
    
    return render(request, 'bookstore/confirm_purchace.html',
                  {'order_fields': order_fields, 'form': form, 'cart_id': cart_item.id})

@login_required
def do_purchase(request, cart_id):
    cart_item = get_object_or_404(CartItem, pk=cart_id)
    if request.method == 'POST':
        order_fields = {
            'user': request.user,
            'book': cart_item.book,
            'quantity': cart_item.quantity,
            'date_added': datetime.datetime.now(),
            'status': OrderItem.PROCESSING,
            'delivery_method': OrderItem.SHIPPING
        }
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = OrderItem.objects.create(**order_fields)
            order.delivery_method = form.cleaned_data['delivery_method']
            order.save()
            CartItem.objects.filter(id=cart_id).delete()
            return redirect('bookstore:thanks')
        return render(request, 'bookstore/confirm_purchace.html',
                      {'form': form})
    else:
        raise Http404('Invalid request method')
    
@login_required
def myorders(request):
    orderlist = OrderItem.objects.all()
    return render(request, 'bookstore/myorders.html', {'orderlist': orderlist})

@login_required
def complete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(OrderItem, id=order_id)
        order.status = OrderItem.COMPLETED
        order.save()
        return redirect('bookstore:myorders')
    else:
        raise Http404('Invalid request method')
        
    
    
