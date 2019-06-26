from django.shortcuts import render, redirect
from django_registration.views import RegistrationView
from django_registration.forms import RegistrationFormUniqueEmail
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_registration.signals import user_registered
import django
from collections import OrderedDict
import datetime

# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            booklist = Book.objects.all()
            words = form.cleaned_data['keywords'].split()
            for word in words:
                booklist = Book.objects.filter(title__icontains=word)
            category = form.cleaned_data['category']
            if category != SearchForm.ALL:
                booklist = booklist.filter(category=category)
    else:
        form = SearchForm()
        booklist = Book.objects.all()
    return render(request, 'bookstore/index.html', {'booklist': booklist, 'form': form})
    # else:
    #     return redirect('bookstore:login')
    
@login_required
def mystore(request):
    booklist = Book.objects.filter(seller=request.user)
    return render(request, 'bookstore/mystore.html', {'booklist': booklist})

@login_required
def user_store(request, username):
    booklist = Book.objects.filter(seller__username=username)
    return render(request, 'bookstore/user_store.html', {'booklist': booklist, 'username': username})
    
@login_required
def mycart(request):
    cartlist = CartItem.objects.filter(user=request.user)
    return render(request, 'bookstore/mycart.html', {'cartlist': cartlist})

@login_required
def mywishlist(request):
    wishlist = WishListItem.objects.filter(user=request.user)
    return render(request, 'bookstore/mywishlist.html', {'wishlist': wishlist})

@login_required
def user_wishlist(request, username):
    wishlist = WishListItem.objects.filter(user__username=username)
    return render(request, 'bookstore/user_wishlist.html', {'wishlist': wishlist, 'username': username})

def thanks(request):
    return render(request, 'bookstore/thanks.html')
    # return HttpResponse('<h1>Thanks!</h1>')

class MyLoginView(auth_views.LoginView):
    # pass
    extra_context = {
        'next': lambda: reverse('bookstore:index')
    }
    
class MyLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('bookstore:index')
    
    
class MyRegistrationView(RegistrationView):
    success_url = reverse_lazy('bookstore:login')
    template_name = 'registration/registration_form.html'
    form_class = RegistrationFormUniqueEmail
    
    def register(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'])
        user_registered.send(self.__class__, user=user)
        return user
    
    
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        # form.seller = request.user
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('bookstore:mystore')
    else:
        form = BookForm()
        
    return render(request, 'bookstore/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save(commit=False)
            book.save()
            return redirect('bookstore:mystore')
    else:
        form = BookForm(instance=book)
    
    return render(
        request,
        'bookstore/edit_book.html',
        {'form': form, 'pk': book.pk})

@login_required
def remove_book(request, book_id):
    if request.method == 'POST':
        books = Book.objects.filter(pk=book_id)
        books.delete()
        return redirect('bookstore:mystore')
    else:
        raise Http404('Invalid query method')
    
@login_required
def increase_quantity(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_id)
        # if cart_item.quantity + amount < 0:
        #     cart_item.quantity = 0
        # else:
        cart_item.quantity += 1
        cart_item.save()
        return redirect('bookstore:mycart')
    else:
        raise Http404('Invalid query method')

@login_required
def decrease_quantity(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_id)
        if cart_item.quantity  > 0:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('bookstore:mycart')
    else:
        raise Http404('Invalid query method')

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
    orderlist = OrderItem.objects.filter(user=request.user).order_by('date_added')
    return render(request, 'bookstore/myorders.html', {'orderlist': orderlist})

@login_required
def received_orders(request):
    orderlist = OrderItem.objects.filter(book__seller=request.user).order_by('date_added')
    return render(request, 'bookstore/received_orders.html', {'orderlist': orderlist})

@login_required
def complete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(OrderItem, id=order_id)
        order.status = OrderItem.COMPLETED
        order.save()
        return redirect('bookstore:myorders')
    else:
        raise Http404('Invalid request method')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    wishlist = WishListItem.objects.filter(user=user)
    context = {
        'username': user.username,
        'email': user.email,
        'wishlist': wishlist
    }
    return render(request, 'bookstore/profile.html', context)

def test(request):
    class TestForm(forms.Form):
        name = forms.CharField(max_length=100)
        hello = forms.CharField(max_length=100)
    form = TestForm()
    return render(request, 'bookstore/test.html', {'form': form})
