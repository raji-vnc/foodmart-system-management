from django.contrib import admin
from .models import Category,Brand,Product,Post,CartItem,Order,OrderItem,Like,Contact,Payment

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Post)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Like)
admin.site.register(Payment)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','created_at')
    search_fields=('name','email')