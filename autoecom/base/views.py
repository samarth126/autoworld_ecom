from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import RForm
from django.contrib import messages
# from django.shortcuts import get_object_or_404, render


# Create your views here.
def home(request):
   
    loop=range(1,8)
    # message = Message.objects.all()
    
    return render(request, 'index.html', {'loop':loop})


def product(request):
    return render(request, 'product.html')


def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

# def login(request):
    
#     login(request)
#     return redirect('home')
    
   

def user_dash(request):
    return render (request, 'user_profile/dashboard.html')

def productlist(request):
    loop=range(1,8)
    return render(request, 'productlist.html', {'loop':loop})

def register(request):
   
    form = RForm()
    if request.method == 'POST':
        form = RForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("new user created")
        else:
            return HttpResponse("not working")
            
          
            
            
            
        
    context={'form':form}
    return render(request, 'loginr.html',context)


def loginr(request):
    if request.user.is_authenticated:
        return HttpResponse("okok")
    if request.method == 'POST':
        emailw = request.POST.get('email')
        passs = request.POST.get('password') 
        try:
            user = User.objects.get(email=emailw)
            
        except:
            messages.error(request, '{} does not exist'.format(emailw))

        user=authenticate(request, email=emailw, password=passs)   
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username password does not exist')

    
   
    # return render(request,'loginr.html', context)
    
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')
