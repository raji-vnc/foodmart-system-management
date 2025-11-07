from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shop.models import Contact,Product,CartItem,Payment
from shop.models import ProductForm

def admin_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request,user)
            return redirect('admin_dashboard')
        else:
            messages.error(request,"invalid credentials or not an admin")
    return render(request,'dashboard/admin_login.html')
    
@login_required(login_url='admin_login')
def admin_dashboard(request):
    contact=Contact.objects.all().order_by('-created_at')
    products=Product.objects.all()
    cartitems=CartItem.objects.all().select_related('product','user')
    payments=Payment.objects.all().order_by('-payment_date')
    return render(request,'dashboard/admin_dashboard.html',{
        'contact':contact,
        'products':products,
         'cartitems':cartitems,
         'payments':payments,
        })
    

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='login')
def add_product(request):
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Product added successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request,'please fix the form errors below')
    else:
        form=ProductForm()
    return render(request,'dashboard/product_form.html',{'form':form,'title':'Add products'})
    

@login_required(login_url='login')
def edit_product(request,id):
    product=get_object_or_404(Product,id=id)
    if request.method =="POST":
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully!")
            return redirect('admin_dashboard')
    else:
        form=ProductForm(instance=product)
    return render(request,'dashboard/product_form.html',{'form':form,"title":'Edit Product'})

@login_required(login_url='admin_login')
def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    messages.success(request,"Product delted successfully")
    return redirect('admin_dashboard')
