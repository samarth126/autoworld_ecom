from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
   
    loop=range(1,8)
    
    return render(request, 'index.html', {'loop':loop})


def product(request):
    return render(request, 'product.html')


def cart(request):
    return render(request, 'cart.html')



def user_dash(request):
    return render (request, 'user_profile/dashboard.html')

def productlist(request):
    loop=range(1,8)
    return render(request, 'productlist.html', {'loop':loop})