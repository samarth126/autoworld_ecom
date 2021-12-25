from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name="home"),
    path('product/',views.product, name="product"),
    path('cart/',views.cart, name="cart"),
    path('userdash/',views.user_dash, name="user profile"),
 


]