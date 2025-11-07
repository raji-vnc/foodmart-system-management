from django import forms
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    image=models.ImageField(upload_to='categories/')
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to='brands/')
    description=models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    # title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.PositiveBigIntegerField(default=0)
    rating=models.DecimalField(max_digits=3,decimal_places=1,default=0)
    unit=models.CharField(max_length=50,default="! UNIT")
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    in_stock=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    brand=models.ForeignKey(Brand,related_name='products',on_delete=models.SET_NULL,null=True,blank=True)

    def discounted_price(self):
        if self.discount>0:
            return self.price-(self.price * self.discount/100)
        return self.price
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,related_name='posts',on_delete=models.SET_NULL,null=True)
    image=models.ImageField(upload_to='blog_images/',blank=True,null=True)
    content=models.TextField()
    excert=models.TextField(blank=True)
    published_date=models.DateField(default=timezone.now)
    created_date=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    is_published=models.BooleanField(default=True)

    class Meta:
        ordering=['-published_date']

    def __str__(self):
        return
    
    def __str__(self):
        return self.title

    
class CartItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='cart_items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("user",'product')
    def subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.product.title}({self.quantity})"

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='orders',on_delete=models.CASCADE)
    creted_at=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=12,decimal_places=2)
    status=models.CharField(max_length=30,default="pending")
    address=models.TextField()
    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    qunatity=models.PositiveBigIntegerField()


class Like(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','product')

    def __str__(self):
        return f"{self.user.username} liked {self.product.name}"
    



class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}- {self.email}"

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','price','category','description','image']

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_status=models.CharField(max_length=50,default='Pending')
    payment_date=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} -₹{self.total_amount} ({self.payment_status})"