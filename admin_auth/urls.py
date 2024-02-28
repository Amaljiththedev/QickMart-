from django.contrib import admin
from django.urls import path,include
from .views import *
from category import views as category_views
from products import views as products_views
urlpatterns = [
    path('',admin_login,name='admin_login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('usermanagement/',User_management,name='user_management'),
    path('status/<int:user_id>/block/',block,name='block_status'),
    path('status/<int:user_id>/unblock/',unblock,name='unblock_status'),
    path('userviewdetails/<int:user_id>/',userviewdetails,name='userviewdetails'),
    path('category/',category_views.category_list,name='category'),
    path('add_category/',category_views.add_category,name='add_category'),
    path('edit_category/<int:id>/',category_views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',category_views.delete_category,name='delete_category'),
    path('block_category/<int:id>/',category_views.block_category,name='block_category'),
    path('unblock_category/<int:id>/',category_views.unblock_category,name='unblock_category'),
    path('product_management/',products_views.product_view,name='product_management'),
    path('add_product/',products_views.add_product,name='add_product'),
    path('edit_product/<int:id>/',products_views.update_product,name='edit'),
    path('add_brand/',category_views.add_brand,name='add_brand'),
    path('block_product/<int:id>/',products_views.block_product,name='block_product'),
    path('unblock_product/<int:id>/',products_views.unblock_product,name='unblock_product'),
    path('delete_product/<int:id>/',products_views.delete_product,name='delete_product'),
    
]
