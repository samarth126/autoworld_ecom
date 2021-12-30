from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name="home"),
    path('product/',views.product, name="product"),
    path('logout/', views.logoutUser, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('userdash/',views.user_dash, name="user profile"),
    path('productlist/', views.productlist, name="productlist"),
    path('register/', views.register, name="register"),
    path('login/', views.loginr, name='loginr'),
 


]