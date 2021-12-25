from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    con=False;
    return render(request, 'index.html', {'con':con})


def product(request):
    return render (request, 'product.html')


def cart(request):
    return render (request, 'cart.html')



def user_dash(request):
    return render (request, 'user_profile/dashboard.html')

