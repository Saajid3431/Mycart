from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.models import Category,Products, Carousal, Cart
from django.shortcuts import get_object_or_404
# Create your views here.

#index page
login_required (login_url='login')
def index(request):
    category = Category.objects.filter(status=0)
    return render(request,'index.html',{"category":category})


#home page
def home(request):
    category=Category.objects.filter(status=0)
    context = {'category' : category}
    return render(request,'home.html',context)


#categories
@login_required(login_url='login')
def category(request):
    category=Category.objects.filter(status=0)
    return render(request,'categories.html',{"category":category})


#signup page
def signupp (request):
    if request.method == "POST":
        username = request. POST ['username']
        email = request. POST ['email']
        password = request.POST ['password']
        if User.objects.filter(username=username).exists ():
            messages.info(request,"*Username already exists")
            return redirect('signup')
        elif User.objects.filter(email=email).exists ():
            messages.info(request,"*User with this Email already exists")
            return redirect('signup')
        else:
            myuser= User.objects.create_user(username=username,email=email,password=password)
            myuser.save()
            return redirect('login')
    else:
        return render(request,'signup.html')


#login page
def loginn(request):
    if request.method == "POST":
        username = request.POST ['username']
        password = request. POST ['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login (request,user)
            return redirect ('home')
        else:
            messages.info(request,"*No user found")
            return redirect ('login')
    
    return render(request,'login.html')


#logout
def logout(request):
    auth.logout(request)
    return redirect (index)


#product page
@login_required(login_url='login')
def products(request,slug):
    if request.user.is_authenticated:
        if (Category.objects.filter(slug=slug,status=0)):
            products=Products.objects.filter(category__slug=slug)
            category= Category.objects.filter(slug=slug)
            category_name=Category.objects.filter(slug=slug).first()
            context={
                 'products' : products,
                 'category_name':category_name,
                 'category' : category,
                }
            return render (request,'products.html',context)
        else:
            return redirect('home')
    else:
        return redirect ('login')
    

#productview
@login_required(login_url='login')
def productview(request,cate_slug,prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Products.objects.filter(slug=prod_slug,status=0)):
            products = Products.objects.filter(slug=prod_slug,status=0).first
            context={'products': products}
        else: 
            # messages.error(request,"No such products found")
            return redirect('products')
    else:
        return redirect('products')
    return render(request,'productview.html',context)


#faqpage
@login_required(login_url='login')
def faq(request):
    if request.user.is_authenticated:
        return render(request,"faq.html")
    else:
        return redirect ('login')
    
#add to cart
def addtocart(request):
    if request.method=='POST' :
        if request.user.is_authenticated:
            prod_id=int (request. POST.get('product_id'))
            product_check = Products.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse ({'status': "product already in cart"})
                else:
                    prod_qty= int(request.POST.get('product_qty'))
                    
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id=prod_id, product_qty=prod_qty)
                        
                        messages.info(request,"*Added to cart successfully")
                    else:
                        messages.info(request,"Only " + str(product_check.quantity + " available"))
            else:
                return JsonResponse ({'status': "No such product"})

        else:
            return JsonResponse ({'status': "Login to continue"})
    
    return redirect('products')

#carousal
@login_required(login_url='login')
def carousal(request):
    dict_carousal ={
        'carousal': Carousal.objects.all()
    }
    return render(request,"home.html",dict_carousal)

# cartpage
def cartview (request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.product_qty > item.product_qty:
            Cart.objects.delete(id=item.id)
    cartitems = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cartitems:
        total_price= total_price + item.product.selling_price * item.product_qty

    context = {'cartitems' : cartitems , 'total_price' : total_price , 'cart' : cart}
    return render(request,"cartview.html",context)

#Quantity update in cart
@login_required(login_url='login')
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status' : "Updated succesfully"})
    return redirect ('home')    

#delete cart item
def deletecartitem(request):
    if request.method == 'POST':
        prod_id =int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user,product_id = prod_id)):
            cartitem= Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status' : "deleted succesfully"})
    return redirect ('home')    


#orderlacing
def placeorder (request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.product_qty > item.product_qty:
            Cart.objects.delete(id=item.id)
    cartitems = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cartitems:
        total_price= total_price + item.product.selling_price * item.product_qty 
        grant_total = int(3) + total_price
    context = {'cartitems' : cartitems , 'total_price' : total_price , 'cart' : cart ,'grant_total' : grant_total}
    return render(request,"placeorder.html",context)


#searchproduct

@login_required(login_url='login')
def productlistajax (request):
    products = Products.objects.filter(status=0).values_list('product_name', flat=True)
    productlist= list(products)
    return JsonResponse (productlist, safe=False)


@login_required(login_url='login')
def searchproduct (request):
    if request.method == "POST":
        searchedterm= request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Products.objects.filter(product_name__contains=searchedterm).first()
            if product:
                return redirect('home/' + product.category.slug + '/' + product.slug)
            else:
                messages.info(request, 'No product for match your serach')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))
    
    