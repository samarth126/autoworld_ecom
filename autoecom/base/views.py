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
from matplotlib.style import context
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import RForm
from django.contrib import messages
from .filters import ProductFilter

from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum 
from Crypto.Cipher import AES
from django.core.paginator import Paginator
from Pdf_so import pdf_so

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
    brad = Product.objects.all().values('brand').distinct()
    cateories = Category.objects.all()
    pro=Product.objects.prefetch_related("product_image").all()
    myFilter=ProductFilter(request.GET, queryset=pro)
    pro=myFilter.qs
   
    loop=range(1,8)
    # message = Message.objects.all()
    
    
    return render(request, 'index.html', {'loop':loop,'products':products,'brad':brad,'cartItems':cartItems, 'cateories':cateories, 'myFilter':myFilter })

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



def cod(request):
    if request.user.is_authenticated:
        customers = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customers, status=False)
        items = order.order_item_set.all()
        print(order.id)
    else:
        items =[]
        order ={'get_cart_total':0, 'get_cart_items':0}
    context={'customers':customers, 'items':items, 'order':order}
    
    
    return render(request, 'cod.html', context)




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




def cod_status(request):
    return render(request, 'cod_status.html')



def update_cod(request):
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

            en=shipping_address(Order=order,Customer=customers,country=country,city=city,state=state,zipcode=zipcode,address=address)
            en.save()
            anni=Order.objects.filter(Customer=customers, status=False).update(price=order.get_cart_total, status=True, cod=True)
            x=str(order.id)
            lp=str(customers.first_name)
            send_mail(
        
                
                'BHARATAUTO SOLUTIONS ORDER confirmed', #subject
                'dear ' + lp + ' ,hello thank you for purchasing from Autoworld, your order id is '+ x,
                'bharatautosolution81@gmail.com', #from email
                [us], #To email
                fail_silently=False
                
            )
            context={'order':order,'us':us}
    return render(request, 'cod_status.html',context)





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
            anni=Order.objects.filter(Customer=customers,status=False).update(price=order.get_cart_total, status=True)
            ob=us
            # res=sendemail(request, ob)
            print(ob)
            # ress=sendemail(request, anni.status)
            
            total_price=order.get_cart_total
            order_id=order.id
            emm=request.user.email
            print(emm)

            # param_dict = {}
            param_dict = {
                
                'MID': Paytm_id,
                'ORDER_ID': str(order_id),
                'TXN_AMOUNT': str(total_price),
                'CUST_ID': str(emm),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

            }
            param_dict['CHECKSUMHASH'] = PaytmChecksum.generateSignature(param_dict, Paytm_Key) 
         

           
            return render(request, 'PaytemRedirect.html', {'param_dict': param_dict})

    context={}
    return render(request, 'checkout.html', context)

# def sendemail(request, us):
#     usrr=us
    
#     send_mail(
        
                
#                 'BHARATAUTO SOLUTIONS ORDER confirmed', #subject
#                 'dear thank you', #message
#                 'priyanshuparashar223@gmail.com', #from email
#                 [usrr.email], #To email
#                 fail_silently=False
                
#             )
    




@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    
    x=request.POST.get('ORDERID')
    bank_name=request.POST.get('BANKNAME')
    bank_txn_id=request.POST.get('BANKTXNID')
    txn_id=request.POST.get('TXNID')
    txn_amt=request.POST.get('TXNAMOUNT')
    txn_date=request.POST.get('TXNDATE')

    
    verify = PaytmChecksum.verifySignature(response_dict, Paytm_Key,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            ann=Order.objects.filter(id=x)
            anni=Order.objects.get(id=x)
            lp=anni.Customer.first_name
            ss=anni.Customer.user
            ann.update(payment_status=True)
            trans=Transaction(order=anni, txn_id=txn_id, bank_txn_id=bank_txn_id, bank_name=bank_name, txn_amt=txn_amt, txn_date=txn_date)
            trans.save()
            send_mail(
        
                
                'Autoworld ORDER confirmed', #subject
                'dear ' + lp + ' ,hello thank you for purchasing from Autoworld, your order id is '+x, #message
                'bharatautosolution81@gmail.com', #from email
                [ss], #To email
                fail_silently=False
                
            )
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
        orders = Order.objects.filter(Customer=cust, status=True).order_by('-id')
        itemes = Order_item.objects.all()
    else:
            return redirect('loginr')
    context =  {'customers':cust, 'orders': orders, 'itemes':itemes,'us':us,'cartItems':cartItems,'messages':messages }
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




def gen_pdf_page(request):

    return render (request, 'pdf_gen.html')



def gen_pdf(request, pd=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        cartItems= nav(HttpRequest, customer)
    else:
        cartItems=0
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    o_id = Order.objects.get(id=pd)
    total=o_id.get_cart_total
    qnt=o_id.get_cart_items
    itemes = Order_item.objects.filter(Order=o_id)
    pdd=[]
    for i in itemes:
        x = Product.objects.get(id=i.Product.id)
        pdd.append(x.title)

    c_name=str(customer.first_name + ' ' + customer.last_name)
    phone=request.user.phone_no
    x=pdf_so.pdff(response,c_name,o_id,pdd,total,phone,qnt)
    context={}
    return x



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
    page_num=request.GET.get('page')
    
    myFilter=ProductFilter(request.GET, queryset=pro)
    from_class=ProductFilter
    pro=myFilter.qs
    cateories = Category.objects.all()
    brad = Product.objects.all().values('brand').distinct()
    porduct_pageinator=Paginator(pro,15)
    page=porduct_pageinator.get_page(page_num)
    BR=Product.objects.all()
    
    context={'product':page, 'myFilter':myFilter,'cartItems':cartItems,'cat':cateories,'br':BR,'brad':brad}
    print(context)
    
    
    
    
    
    
    
    q = request.GET.get('q')
    
    
    if request.GET.get('q') == None:
        
        products=Product.objects.prefetch_related("product_image").all()
        
        
    else:
        products=Product.objects.prefetch_related("product_image").filter(
            
            Q(title__icontains=q) |
            Q(desc__icontains=q)  |
            Q(vmodel__model_name__icontains=q) |
            Q(vehicaltype__type_of__icontains=q) |
            Q(category__name__icontains=q)
            
            
        )
        page_num=request.GET.get('page')
        porduct_pageinator=Paginator(products,1)
        page=porduct_pageinator.get_page(page_num)
        page=porduct_pageinator.get_page(page_num)
        brad = Product.objects.all().values('brand').distinct()
        
        
        cateories = Category.objects.all()
        BR=Product.objects.all()
        return render(request, 'products.html', {'brad':brad,'product':page, 'myFilter':myFilter,'cat':cateories, 'br':BR})
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



def category(request, slug=None, kt=None):
    if kt == 'brand':
        products=Product.objects.filter(brand=slug)
        page="brand"
        cateories = Category.objects.all()
        brad = Product.objects.all().values('brand').distinct()
        
        
    else:
        
        cate=Category.objects.get(slug=slug)
        products=Product.objects.filter(category=cate.id)
        print (slug)
        page="cate"
        cateories = Category.objects.all()
        brad = Product.objects.all().values('brand').distinct()

    return render(request, 'category.html', {'pro':products,'cat':cateories,'brad':brad, 'page':page})


  
  

def about(request):
    return render(request, 'about.html')


def privacy(request):
    return render(request, 'privacy.html')


def support(request):
    if request.user.is_authenticated:
        sen=request.user
        customer = request.user.customer
        if request.method == 'POST':
            s_name=request.POST.get('s_name')
            s_email=request.POST.get('s_email')
            s_message=request.POST.get('s_message')
            s_detail=request.POST.get('s_detail')

            en=Support(sender=customer ,s_name=s_name, s_email=s_email, s_message=s_message, s_detail=s_detail)
            en.save()
                
                
                
            send_mail(
        
                
                'BHARATAUTO SOLUTIONS ORDER confirmed', #subject
                'hello thank you for purchasing order id is ', #message
                'bharatautosolution81@gmail.com', #from email
                [sen], #To email
                fail_silently=False
                
            )

            return redirect('home')
    
    return render(request, 'support.html')



def contact(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_no=request.POST.get('phone_no')
        message=request.POST.get('message')
        enn=Contact(name=name,email=email,phone_no=phone_no,message=message)
        enn.save()
        return redirect('home')
    return render(request, 'support.html')




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
        return redirect('home')
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
    cat=Category.objects.all()
    
    
    return render(request, 'a.html', {'cat':cat})
    # if request.user.is_authenticated:
    #     us=request.user
    #     cus=Customer.objects.get(user=us)
    #     oor=Order.objects.filter(Customer=cus)
        
        
        
        
        
    #     dic={}
        
    #     for k in oor:
    #         ok=Order_item.objects.filter(Order=k)
            
    #         for o in ok:
    #             dic[o]=o.Product
               
            
            
        
        
            
    #         # dic[k]=(Order_item.objects.filter(Order=k))
    #     print(ok)
    # x=4           
        
            
                        
            
        
              
          
            
                
                
            
         
        
        
        
        
            
        
        
        
  

    
    # return render(request, 'a.html', {'dic':dic,'x':x})


