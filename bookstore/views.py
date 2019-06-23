from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse
from django.contrib.auth import views as auth_views

# Create your views here.

def index(request):
    
    if request.user.is_authenticated:
        booklist = Book.objects.all()
        return render(request, 'bookstore/index.html', {'booklist': booklist})
    else:
        return redirect('bookstore:login')
    
def mystore(request):
    if request.user.is_authenticated:
        booklist = Book.objects.filter(seller=request.user)
        return render(request, 'bookstore/mystore.html', {'booklist': booklist})
    else:
        return redirect('bookstore:login')
    
    

def thanks(request):
    return HttpResponse('<h1>Thanks!</h1>')

class MyLoginView(auth_views.LoginView):
    # pass
    extra_context = {
        'next': lambda: reverse('bookstore:index')
    }
    
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bookstore:index')
    else:
        form = BookForm()
        
    return render(request, 'bookstore/add_book.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookstore:index')
    else:
        form = BookForm(instance=book)
    
    return render(
        request,
        'bookstore/edit_book.html',
        {'form': form, 'pk': book.pk})
    
    
