from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name="home"),
    path('login/',views.login, name="login"),
    path('product/',views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('userdash/',views.user_dash, name="user profile"),
    path('productlist/', views.productlist, name="productlist"),
 


]