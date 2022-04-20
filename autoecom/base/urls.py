from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name="home"),
    path('product/<str:pk>',views.product, name="product"),
    path('logout/', views.logoutUser, name="logout"),
   
   
    # path('productlist/<str:pk>/', views.productlist, name="productlist"),
    path('products/', views.products, name="products"),
    path('register/', views.register, name="register"),
    path('login/', views.loginr, name='loginr'),
    
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('cod/', views.cod, name="cod"),
    path('codstatus/', views.cod_status, name="cod_status"),

    path('update_cod/',views.update_cod, name="update_cod"),


    path('update_checkout/',views.update_checkout, name="update_checkout"),

    path('update_item/', views.updateItem, name="update_item"),

    path('userdash/',views.user_dash, name="user_profile"),
    path('update_acc/',views.update_acc, name="update_acc"),
    # path('cat/<slug:slug>/', views.cat, name='cat'),
    path('type/', views.type, name='type'),
    path('a/', views.a, name='a'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('support/', views.support, name='support'),
    path('contact/', views.contact, name='contact'),

    path('gen_pdf/<str:pd>', views.gen_pdf, name='gen_pdf'),
    path('gen_pdf_page/', views.gen_pdf_page, name='gen_pdf_page'),

    path('category/<slug:slug>/<str:kt>/', views.category, name='category'),
    
    

    path('brand/<slug:slug>/<str:pk>/', views.brand, name='brand'),
    path('model/<slug:slug>/<str:pk>/', views.model, name='model'),
    path('year/<slug:slug>/<str:pk>/', views.myear, name='myear'),

    #Paytm
    # path('/', views.a, name='a'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    
]