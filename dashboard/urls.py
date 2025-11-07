from django.urls import path
from .import views
urlpatterns=[
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),

#product crud operations
path('admin/product/add/',views.add_product,name='add_product'),
path('admin/product/edit/<int:id>/',views.edit_product,name='edit_product'),
path('admin/product/delete/<int:id>/',views.delete_product,name='delete_product'),
]