from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse
from django.contrib.auth import views as auth_views

# Create your views here.

def index(request):
    
    if request.user.is_authenticated:
        return render(request, 'bookstore/index.html')
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
        form = BookForm(request.POST)
        form.save()
        
    
