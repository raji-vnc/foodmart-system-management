from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Brand,Post,CartItem,Order,OrderItem,Like,Contact,Payment
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from stripe.oauth_error import StripeError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
stripe.api_key=settings.STRIPE_SECRET_KEY
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
import uuid

def register_user(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password!=confirm_password:
            return render(request,'register.html',{'error':'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request,'register.html',{'error':'Username already taken'})
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('login')
    return render(request,'register.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return render(request,'login.html',{'error':'Invalid credentials'})
    return render(request,'login.html')
def logout_user(request):
    logout(request)
    return redirect('login')
def index(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    brands=Brand.objects.all()
    posts=Post.objects.all()
    cartitems=CartItem.objects.all()
    orders=Order.objects.all()
    orderitems=OrderItem.objects.all()
    context={
        'products':products,
        'categories':categories,
        'brands':brands,
        'posts':posts,
        'caritem':cartitems,
        'order':orders,
        'orderitem':orderitems,
    }
    return render(request,'shop/index.html',context)

def add_single_product(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    context={
        'product':product,

    }
    return render(request,'singleproduct/index.html',context)
@login_required(login_url='login')
def add_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart_item, created=CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity':1}
        )
    if not created:
            cart_item.quantity +=1
            cart_item.save()
        
        
    return redirect('view_cart')

def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum(item.product.price*item.quantity for item in  cart_items)
    return render(request,'cart/cart.html',{'cart_items':cart_items,"total":total})


def increase_quantity(request,product_id):
    cart_item,created=CartItem.objects.get_or_create(product_id=product_id,user=request.user)
    cart_item.quantity +=1
    cart_item.save()
    return redirect('view_cart')

def decrease_quantity(request,product_id):
    cart_item=get_object_or_404(CartItem,product_id=product_id,user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('view_cart')
        

    
def remove_from_cart(request,product_id):
    item=get_object_or_404(CartItem,id=product_id,user=request.user)
    item.delete()
    return redirect('view_cart')
    
   
def create_order(request):
    cart_items=CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('view_cart')
    
    total=sum(item.product.price * item.quantity for item in cart_items)
    order=Order.objects.create(user=request.user,total_price=total)

    for item in cart_items:
        OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
        cart_items.delete()


        return redirect('order_detail',order_id=order.id)


def order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    order_items=order.items.all()
    return render(request,'order/order.html',{'order':order,'order_items':order_items})

def checkout(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'payment/index.html',{'cart_items':cart_items,'total':total})
@login_required(login_url='login')
def payment(request):
    total_amount = 10000  # 100 rupees = 100 * 100 paise
    intent = stripe.PaymentIntent.create(
        amount=total_amount,
        currency='inr',
        automatic_payment_methods={'enabled': True},
        metadata={'user_id':request.user.id},  
    )
    return render(request, 'payment/index.html', {
        'client_secret': intent.client_secret,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })
def payment_success(request):
    latest_payment=Payment.objects.filter(user=request.user).order_by('-payment_date').first()
    if not latest_payment:
        return redirect('view_cart')
    context={
        'payment':latest_payment,
        'total':latest_payment.total_amount,
    }
    return render(request,'payment/payment_success.html',context)
@login_required(login_url='login')
def dummy_cv_success(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum(item.product.price * item.quantity for item in cart_items)
    if request.method=="POST":
        cvc=request.POST.get('cvc','').strip()
        if not cvc or not cvc.isdigit() or len(cvc) not in(3,4):
            messages.error(request,"Enter a valid CVC (3 or 4 digits).")
            return redirect("dummy_cvc_payment")
        fake_txn="DUMMY-STRIPE-"+ uuid.uuid4().hex[:8].upper()
        payment=Payment.objects.create(
            user=request.user,
            total_amount=total,
            payment_status="completed",
            transaction_id=fake_txn
        )
        cart_items.delete()

        messages.success(request,"Dummy pament successful(no real charge).")
        return redirect('payment_success')
    return render(request,'payment/dummy_cvc.html',{'total':total,})

 
 


@login_required(login_url='login')
def wishlist_page(request):
    wishlist_items=Like.objects.filter(user=request.user).select_related('product')
    return render(request,'wishlist/index.html',{'wishlist_items':wishlist_items})


@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    wishlist_item, created = Like.objects.get_or_create(user=user, product=product)

    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'added'})


@login_required(login_url='login')
def profile_page(request):
    user=request.user
    return render(request,'profile.html',{'user':user})


# @login_required(login_url='login')
# def contact_us(request):
#     if request.method=="POST":
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         message=request.POST.get('message')
#         messages.success(request,'Your message has been sent successfully')
#         return redirect('contact')
#     return render(request,'contact/contact.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        Contact.objects.create(name=name,email=email,message=message)
        subject=f"New Contact Message from{name}"
        body=f"{name}\nEmail:{email}\n\nMessage:\n{message}"
        try:
            send_mail(subject,body,settings.EMAIL_HOST_USER,['rajivn@gmail.com'],
                      fail_silently=False,)
            message.success(request,'Your message has been sent sucessfully')
        except Exception as e:
            message.error(request,'sorry, somthing went wrong,Please try again later.')
        return render(request,'contact/contact.html')
    return render(request,'contact/contact.html')