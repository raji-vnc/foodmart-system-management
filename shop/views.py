from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Brand,Post,CartItem,Order,OrderItem
from django.contrib import messages

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
        'brand':brands,
        'posts':posts,
        'caritem':cartitems,
        'order':orders,
        'orderitem':orderitems,
    }
    return render(request,'shop/index.html',context)

def add_single_product(request,product_id):
    product=get_object_or_404(Product,product_id=product_id)
    context={
        'product':product
    }
    return render(request,'singleproduct/index.html',context)

def add_cart(request,product_id):
    product=get_object_or_404(Product,product_id=product_id)
    if request.user.is_authenticated:
        cart_item, created=CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity +=1
            cart_item.save()
        
        messages.success(request,f"{product.name}added to your cart")
    else:
        messages.error(request,"Please log in to add items to your cart.")

        return redirect('add_single_product',product_id=product_id)

def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum(item.subtotal() for item in cart_items)
    return render(request,'cart/cart.html',{'cart_items':cart_items,'total':total})


def increase_qunatity(request,product_id):
    item=get_object_or_404(CartItem,id=product_id,user=request.user)
    item.quantity +=1
    item.save()
    return redirect('view_cart')

def decrease_quantity(request,product_id):
    item=get_object_or_404(CartItem,id=product_id,user=request.user)
    if item.quantity >1:
        item.quantity -=1
        item.save()

    else:
        item.delete()
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
