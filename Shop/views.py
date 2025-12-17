from django.shortcuts import render, redirect
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product


# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all() 
    return render(request, 'shop/index.html', {"products":products, "categories":categories})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, "Invalid login details")
    return render(request, 'Shop/login.html')



def register(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/register')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('/register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=fullname)
        user.save()
        
        # Redirect to login page after successful registration
        return redirect('shop:login')
    
    return render(request, 'shop/register.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# def cart(request):
#     return render(request, 'Shop/cart.html')


def orders(request):
    return render(request, 'Shop/orders.html')


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart = None
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        try:
            cart_item = CartItem.objects.get(user=request.user, product=product, cart=cart)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart)
    else: 
        return redirect('login')
    return redirect('shop:home')



def view_cart(request):
    if request.user.is_authenticated:
        cart = None
        cart_items = None
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        
        cart_items = CartItem.objects.filter(user=request.user, cart=cart)
    else:
        return redirect('login')

    return render(request, "shop/cart.html", {"cart":cart, "cart_items":cart_items})


def delete_item(request, id):
    item = CartItem.objects.get(id=id)
    item.delete()
    return redirect('shop:view_cart')

def decrease_item(request, id):
    item = CartItem.objects.get(id=id)
    item.quantity -= 1    

    if item.quantity <= 1:
        item.quantity = 1
    item.save()
    return redirect('shop:view_cart')
       

def increase_item(request, id):
    item = CartItem.objects.get(id=id)
    item.quantity += 1
    item.save()

    return redirect('shop:view_cart')


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user)
    for cart_item in cart.cart_items.all():
        order_item = OrderItem.objects.create(order=order, product=cart_item.product, user=request.user, discount=0, quantity=cart_item.quantity)
        cart_item.delete()
    return redirect("shop:home")

def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "shop/orders.html", {"orders": orders})

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order/detail.html', {"order": order})

