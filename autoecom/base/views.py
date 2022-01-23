from django.http import request
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
import json
from django.core.mail import send_mail
from django.db.models import *
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import RForm
from django.contrib import messages
from .filters import ProductFilter

from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum 
from Crypto.Cipher import AES

# from django.shortcuts import get_object_or_404, render

Paytm_id = 'rKiFJS58028658686652'
Paytm_Key = 'EJpp@I3%eABmW8S%'



# from django.shortcuts import get_object_or_404, render
def nav(request,customer):
    order, created = Order.objects.get_or_create(Customer=customer, status=False)
    # items = order.order_item_set.all()
    cartItems = order.get_cart_items
    return cartItems

#
# 
#    if request.user.is_authenticated:
#         us= request.user
#         cust, created = Customer.objects.get_or_create(user=us)
#         cartItems= nav(HttpRequest, cust)
#         # cust = request.user.customer
#         # f = shipping_address.objects.get(Customer=cust.id)
#         orders = Order.objects.filter(Customer=cust, status=True)
#         itemes = Order_item.objects.all()
#     else:
#             return redirect('loginr')
def home(request):
    if request.user.is_authenticated:
        us= request.user
        cust, created = Customer.objects.get_or_create(user=us)
        customer = request.user.customer
        cartItems= nav(HttpRequest, customer)
    else:
        cartItems=0
        
    
    products = Product.objects.all()
    cateories = Category.objects.all()
    pro=Product.objects.prefetch_related("product_image").all()
    myFilter=ProductFilter(request.GET, queryset=pro)
    pro=myFilter.qs
   
    loop=range(1,8)
    # message = Message.objects.all()
    
    return render(request, 'index.html', {'loop':loop,'products':products,'cartItems':cartItems, 'cateories':cateories, 'myFilter':myFilter })

def cart(request):
    if request.user.is_authenticated:
        us=request.user
        customer = request.user.customer
        print(us.email)
        cartItems= nav(HttpRequest, customer)
        order, created = Order.objects.get_or_create(Customer=customer, status=False)
        items = order.order_item_set.all()
    else:
        items =[]
        order ={'get_cart_total':0, 'get_cart_items':0}
        cartItems=0
    context={'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'cart.html', context)







def checkout(request):
     if request.user.is_authenticated:
        customers = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customers, status=False)
        items = order.order_item_set.all()
        print(order.id)
     else:
        items =[]
        order ={'get_cart_total':0, 'get_cart_items':0}
     context={'customers':customers, 'items':items, 'order':order}
     return render(request, 'checkout.html', context)




def update_checkout(request):
    if request.user.is_authenticated:
        us = request.user
        customers = request.user.customer
        order = Order.objects.get(Customer=customers, status=False)
        if request.method=="POST":
            address=request.POST.get('address')
            country=request.POST.get('country')
            city=request.POST.get('city')
            state=request.POST.get('state')
            zipcode=request.POST.get('zipcode')

            print(order.get_cart_total)
            print(country)
            en=shipping_address(Order=order,Customer=customers,country=country,city=city,state=state,zipcode=zipcode,address=address)
            en.save()
            anni=Order.objects.filter(Customer=customers).update(price=order.get_cart_total, status=True)
            ob=us
            res=sendemail(request, ob)
            print(ob)
            # ress=sendemail(request, anni.status)
            
            total_price=order.get_cart_total
            order_id=order.id

            # param_dict = {}
            param_dict = {

                'MID': Paytm_id,
                'ORDER_ID': str(order_id),
                'TXN_AMOUNT': str(total_price),
                'CUST_ID': str(request.user.email),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

            }
            param_dict['CHECKSUMHASH'] = PaytmChecksum.generateSignature(param_dict, Paytm_Key) 
         

           
            return render(request, 'PaytemRedirect.html', {'param_dict': param_dict})

    context={}
    return render(request, 'checkout.html', context)

def sendemail(request, us):
    usrr=us
    
    send_mail(
        
                
                'BHARATAUTO SOLUTIONS ORDER confirmed', #subject
                'dear thank you', #message
                'priyanshuparashar223@gmail.com', #from email
                [usrr.email], #To email
                fail_silently=False
                
            )
    
    
    


@csrf_exempt
def handlerequest(request):
  
    
    # customers = request.user.customer
    # order = Order.objects.get(Customer=customers, status=False)
    
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = PaytmChecksum.verifySignature(response_dict, Paytm_Key,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
   
            # return HttpResponse('thanks for your mail')
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            # order_status=False
            # respons=sendemail(request, order_status)
    return render(request, 'paymentstatus.html', {'response': response_dict})





    
 


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('product_id:', productId)


    customer =request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(Customer=customer, status=False)

    order_item, created = Order_item.objects.get_or_create(Order=order, Product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if action == 'delete':
        order_item.delete()

    if order_item.quantity <= 0:
        order_item.delete()


    return JsonResponse('Item was added', safe=False)




def user_dash(request):
    if request.user.is_authenticated:
        us= request.user
        cust, created = Customer.objects.get_or_create(user=us)
        cartItems= nav(HttpRequest, cust)
        # cust = request.user.customer
        # f = shipping_address.objects.get(Customer=cust.id)
        messages = Message.objects.filter(Customer=cust)
        orders = Order.objects.filter(Customer=cust, status=True)
        itemes = Order_item.objects.all()
    else:
            return redirect('loginr')
    context =  {'customers':cust, ' orders': orders, 'itemes':itemes,'us':us,'cartItems':cartItems,'messages':messages }
    return render (request, 'user_profile/dashboard.html',context)







# this just the post request on userdash to update a customer name and other things

def update_acc(request):
    
    if request.user.is_authenticated:
        
             us = request.user
             if request.method=="POST":
                fname=request.POST.get('fname')
                lname=request.POST.get('lname')
                phone=request.POST.get('phone')
                cust=Customer.objects.filter(user=us).update(first_name=fname, last_name=lname)
                # en=cust(first_name=fname, last_name=lname)
                return redirect('user_profile')


    return render (request, 'user_profile/dashboard.html')




def product(request, pk=None):
     if request.user.is_authenticated:
        customer = request.user.customer
        cartItems= nav(HttpRequest, customer)
     else:
        cartItems=0
     product=Product.objects.prefetch_related("product_image").filter(id=pk)
     cateories = Category.objects.all()
     context={'pro':product,'cartItems':cartItems,'cateories':cateories}
     return render(request, 'product.html', context)






# def login(request):
    
#     login(request)
#     return redirect('home')

# def search(request):
    
#     products=Product.objects.all()
#     myFilter=ProductFilter(request.GET, queryset=products)
#     products=myFilter.qs
#     context={'product':products, 'myFilter':myFilter}
#     print(context)
#     return render(request, 'products.html', context) 
    
    
    
def products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cartItems= nav(HttpRequest, customer)
    else:
        cartItems=0
    pro=Product.objects.prefetch_related("product_image").all()
    myFilter=ProductFilter(request.GET, queryset=pro)
    pro=myFilter.qs
    cateories = Category.objects.all()
    context={'product':pro, 'myFilter':myFilter,'cartItems':cartItems,'cateories':cateories}
    print(context)
    
    
    
    
    
    
    
    q = request.GET.get('q')
    
    
    if request.GET.get('q') == None:
        
        products=Product.objects.prefetch_related("product_image").all()
        
        
    else:
        products=Product.objects.prefetch_related("product_image").filter(
            
            Q(title__icontains=q) |
            Q(desc__icontains=q)  |
            Q(vmodel__model_name__icontains=q)
            
            
        )
        print(products)
        return render(request, 'products.html', {'product':products, 'myFilter':myFilter})
    return render(request, 'products.html', context)   
  
        
    
    
    
    
    
   



# def productlist(request, pk=None):
#     products=Product.objects.filter(myear=pk)
    
    
#     loop=range(1,8)
#     return render(request, 'productlist.html', {'pro':products})

# def cat(request, slug=None, Vtype=None):
#     vehicletype=TypeOfVehicle.objects.all()
    
    
    
#     manu=Manufacturer.objects.all()
#     # vmodel=CarModel.objects.filter(manufacturer=pk)
#     # vyear=Year.objects.all().filter(id=pk)
    
#     # context={'Vtype':vehicletype, 'brand':manu, 'vmodel':vmodel, 'vyear':vyear}
#     # print(manu)
#     context={'Vtype':vehicletype, 'manu':manu}
    
#     return render(request, 'cat.html', context)





def type(request, slug=None,  *args, **kwargs):
    if slug is not None:
        manu=Manufacturer.objects.filter(slug=slug)
        print(manu)
        print(slug)
        
        print("working")
        return HttpResponse('hello world')
        
            
        
        
    
        
    vehicletype=TypeOfVehicle.objects.all()
    context={'Vtype':vehicletype}
    
    return render(request, 'type.html', context)
      



def brand(request, slug=None, pk=None, *args, **kwargs):
    
    print(slug)
    # vehicaltype
    manu=Manufacturer.objects.filter(vehicaltype=pk)
    print(pk)
    print(manu)
    
 
    context={'brand':manu}
    
    return render(request, 'brand.html', context)




def model(request, slug=None, pk=None, *args, **kwargs):
    page='model'
    vmodel=CarModel.objects.filter(manufacturer=pk)
    print(vmodel)
    context={'vmodel':vmodel, 'page':page}
    
    return render(request, 'models.html', context)





def myear(request, slug=None, pk=None, *args, **kwargs):
    
    print(slug)
    print(pk)
    products=Product.objects.filter(myear=pk)
    print(product)
    ye=Year.objects.filter(carmodel=pk)
    print(ye)
    
    # context={'year': ye }
    
    
    return render(request, 'models.html', {'year': ye , 'pro':products})



def category(request, slug=None):
    cate=Category.objects.get(slug=slug)
    products=Product.objects.filter(category=cate.id)
    print (slug)
    return render(request, 'category.html', {'pro':products})












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






def a(request):
    loop=range(1,8)

    
    return render(request, 'a.html', {'loop':loop})


