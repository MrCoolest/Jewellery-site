# Importing
import json
from math import fabs
from wsgiref.util import request_uri
# from django import http
from django.contrib.messages.api import error
from django.http import response, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from .models import *
import random
from .form import Registration
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime




# Create your views here.

def index(request):
    display = []
    random_idx =  random.sample(range(0, Product.objects.filter(specail_prod = False).count() - 1), 12)
    for i in random_idx:
        random_object = Product.objects.all()[i]
        display.append(random_object)
    specials = Product.objects.filter(specail_prod = True)    
    show = {'display' : display,'specials':specials, 'full_nav' : True}
    if request.method == "POST":
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        phone = request.POST.get('phone')
        msg = request.POST.get('message')

        Contact_Form(name = name, Email = email, phone=phone , message = msg)

        mess = f"Name : {name}\nEmail : {email}\nPhone : {phone}\nMessage : {msg}"
        send_mail(
                "From Mumbai Fashion",
                mess,
                settings.EMAIL_HOST_USER,
                ["Ankitpatwa3333333@gmail.com"],
                fail_silently= False
            )

    return render(request,'index.html',show)



def loginUser(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username = get_usr)
            if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request,user)
                return redirect('/')
            else:
                messages.warning(request, f'You Entered Wrong OTP! Re-enter Please')
                return render(request,'login.html',{'otp' : True,'usr':usr})
        username = request.POST.get('email')
        password = request.POST.get('passwd')
        # print(username, password)   
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            # player, created = Customer.objects.get_or_create(user=request.user)
            login(request,user)
            return redirect('/')
        elif not User.objects.filter(username = username).exists():
            messages.error(request, f"Incorrect email or password.")
            return redirect('login')
        elif not User.objects.get(username = username).is_active:
            usr = User.objects.get(username = username)
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user = usr, otp=usr_otp)
            mess = f"Hello {usr.first_name}.\n Your OTP is {usr_otp}\n Thanks!"

            # For Sneding Mail
            send_mail(
                "Welcome To Mumbai Fashion",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
            )
            return render(request,'login.html',{'otp' : True,'usr':usr})
        else:
            messages.error(request, f"Incorrect email or password.")
            return redirect('login')

    return render(request, 'login.html')



def logoutUser(request):
    logout(request)
    return redirect('/')



def register(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username = get_usr)
            if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'Welcome! Account has been Created for {usr.username}')
                return redirect('login')
            else:
                messages.warning(request, f'You Entered Wrong OTP! Re-enter Please')
                return render(request,'register.html',{'otp' : True,'usr':usr})

        form = Registration(request.POST)
        # print(form)
        if form.is_valid():
            # print("yess")
            form.save() 
            username = form.cleaned_data.get('username')
            usr = User.objects.get(username = username)
            usr.email = username
            usr.is_active = False
            usr.save()
            customer = Customer(user = usr,name = usr.first_name, email = usr.email) 
            customer.save()
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user = usr, otp=usr_otp)
            mess = f"Hello {usr.first_name}.\n Your OTP is {usr_otp}\n Thanks!"

            # For Sending Mail
            send_mail(
                "Welcome To Mumbai Fashion",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
            )

            return render(request,'register.html',{'otp' : True,'usr':usr})
        else:
            print(form.errors)    
            err = form.errors
            return render(request,'register.html',{'form' : form,'err' : err})
    else:
        form = Registration()
    return render(request,'register.html',{'form' : form})
 


def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
            usr = User.objects.get(username = get_usr)
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user = usr, otp=usr_otp)
            mess = f"Hello {usr.first_name}.\n Your OTP is {usr_otp}\n Thanks!"

            # For Sneding Mail
            send_mail(
                "Welcome To Mumbai Fashion",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
            )
            return HttpResponse("Resend")    
        return HttpResponse("Can't Send")
# def forgot(request):
#     return render(request,"forget_passwd.html")



def productView(request,prod_id):
    # Particular Product
    show = Product.objects.filter(product_id = prod_id)
    

    # Random Product
    display = []
    random_idx =  random.sample(range(0, Product.objects.count() - 1), 5)
    for i in random_idx:
        random_object = Product.objects.all()[i]
        display.append(random_object)

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(product_id = prod_id)
        order, created = Cart.objects.get_or_create(customer = customer, complete=False)
        cartitem, created = CartItem.objects.get_or_create(order=order, product=product)
        itemss = cartitem.quantity
    else:
        itemss = 0
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitem = order['get_cart_items']


    return render(request,"productView.html",{'show':show[0],'display' : display,'itemss':itemss})



def products(request):
    products = Product.objects.all()
    show = {'products' : products, 'heading': 'Products'}
    return render(request,'products.html',show)



def necklaces(request):
    products = Product.objects.filter(category='Necklace')
    show = {'products' : products, 'heading': 'Necklace'}
    return render(request,'products.html',show)



def rings(request):
    products = Product.objects.filter(category='Ring')
    show = {'products' : products, 'heading': 'Rings'}
    return render(request,'products.html',show)



def earings(request):
    products = Product.objects.filter(category='Earings')
    show = {'products' : products, 'heading': 'Earings'}
    return render(request,'products.html',show)



def bangles(request):
    products = Product.objects.filter(category='Bangles')
    show = {'products' : products, 'heading': 'Bangles'}
    return render(request,'products.html',show)



def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Cart.objects.get_or_create(customer = customer, complete=False)
    #     items = order.cartitem_set.all()
    #     cartitem = order.get_cart_items
    # else:
    #     items = []    
    #     order = {'get_cart_total':0, 'get_cart_items':0}
    #     cartitem = order['get_cart_items']

    # context = {'items':items, 'order':order,'cartitem': cartitem}    

    name = Customer.objects.get(user = request.user).id
    sh_Address = ShippingAddress.objects.filter(customer = name)
    

    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            name=request.POST.get('user_name', request.user.first_name)
            email=request.POST.get('user_email', request.user.email)
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pincode=request.POST.get('pin-code')

            order, created = Cart.objects.get_or_create(customer = customer, complete = False)
            # orders = order.cartitem_set.all()
            shipping = ShippingAddress(customer = customer, order = order ,address = address,city = city, state =state, pincode= pincode, phone_number = phone, )
            shipping.save()    

            transaction = datetime.datetime.now().timestamp() 
            order.transaction = transaction
            order.complete = True
            
            order.save()
            # cartitems, created = CartItem.objects.get_or_create(order=order)
            # items = cartitems.cartitem_set.all()
            # items.delete()
            
            thanks = True
            return render(request, 'cart.html', {'thanks':thanks})

    return render(request, 'cart.html', {'old_address' : sh_Address})



def checkout(request):
    return render(request, "checkout.html")

    

@csrf_exempt
def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    # print('Action :', action)

    # print('Product :', productId)

    customer = request.user.customer
    product = Product.objects.get(product_id = productId)
    order, created = Cart.objects.get_or_create(customer = customer, complete=False)

    cartitem, created = CartItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        cartitem.quantity = (cartitem.quantity + 1)
    elif action == 'remove':
        cartitem.quantity = (cartitem.quantity - 1)

    cartitem.save()
    
    if cartitem.quantity <= 0:
        cartitem.delete()

    return JsonResponse("item was added", safe=False)