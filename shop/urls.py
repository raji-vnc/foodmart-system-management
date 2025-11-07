from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='home'),
    path('add_singleproduct/<int:product_id>/',views.add_single_product,name='singleproduct'),
    path('cart/add-to-cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('cart/',views.view_cart,name='view_cart'),
    path('cart/increase/<int:product_id>/',views.increase_quantity,name='increase_quantity'),
    path('cart/decrease/<int:product_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('cart/remove/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('create/',views.create_order,name='create_order'),
    path('<int:order_id>/',views.order_detail,name='order_detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('wishlist_page/',views.wishlist_page,name='wishlist_page'),
    path('toggle-wishlist/<int:product_id>/',views.toggle_wishlist,name='toggle_wishlist'),
   path('register/',views.register_user,name='register'),
   path('login/',views.login_user,name='login'),
   path('logout/',views.logout_user,name='logout'),
 path('profile/',views.profile_page,name='profile'),
 path('contact/',views.contact,name='contact'),
 path('payment/',views.payment,name='payment'),
 path("payment/payment_success/",views.payment_success,name="payment_success"),
 path('payment/success/',views.dummy_cv_success,name='dummy_cv_success'),
    ]