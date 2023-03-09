from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Product, Cart


# Create your views here.

def home(request):
    if request.method == "POST":
        search = request.POST.get("search")
        chair = Product.objects.filter(name__icontains=search)
        sofa = Product.objects.filter(name__icontains=search)
        print(chair)
    else:
        chair = Product.objects.filter(category="Chair")
        sofa = Product.objects.filter(category="Sofa")
    return render(request, 'home.html', locals())


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login succeeded')
            return redirect('home')
        else:
            messages.warning(request, 'User not found! Please a create a new account')
            return render(request, 'registration.html')
    return render(request, 'login.html')


def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Account already exists')
                return redirect('registration')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email,
                                                password=password).save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')
    return render(request, 'registration.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

def product(request):
    return render(request, 'single-product.html', locals())

@login_required(login_url='login')
def checkout(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'checkout.html', locals())


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.00
        shipping_amount = 60.00
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.amount)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request, 'checkout.html', {'cart': cart, 'total_amount': total_amount, 'amount': amount})
        else:
            return render(request, 'home.html')

def search(request):
    if request.method == "GET":
        name = request.GET.get("search")
        product = Product.objects.filter(name__icontains = name)
    return render(request, 'search.html', locals())


def add_products(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category =request.POST.get("category0")
        image = request.FILES.get('image')

        add = Product.objects.create(name=name, price=price, description=description, category=category, product_image=image)
        add.save()
        return redirect('home')

    return render(request, 'add-products.html')

def update_products(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        newname = request.POST.get('name')
        newprice = request.POST.get('price')
        newdescription = request.POST.get('description')
        newimage = request.FILES.get('image')

        product.name = newname
        product.price = newprice
        product.description = newdescription
        product.product_image = newimage
        product.save()
        return redirect('home')

    return render(request, 'update-products.html', {"product":product})
