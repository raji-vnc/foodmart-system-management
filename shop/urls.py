from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='home'),
    path('add_singleproduct/<int:product_id',views.add_single_product,name='singleproduct'),
    path('cart/add-to-cart/<int:product_id/',views.add_cart,name='add_cart'),
    path('cart/',views.view_cart,name='view_cart'),
    path('cart/increase/<int:product_id>/',views.increase_qunatity,name='increase_qunatity'),
    path('cart/decrease/<int:product_id>/',views.decrease_quantity,name='decrease_qunatity'),
    path('cart/remove/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('cre' \
    '')
    ]