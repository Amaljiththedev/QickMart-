from django.contrib import admin
from django.urls import path,include
from admin_auth import views
from django.conf import settings
from django.conf.urls.static import static
from admin_auth import views
from user_auth import views

urlpatterns = [
    path('user_product_view/<int:id>',views.user_product_view,name='user_product_view'),
    path('user_product_list',views.list_of_products,name='user_product_list'),
    path('search/',views.search,name='search'),
    path('get_variant_details/', views.get_variant_details, name='get_variant_details'),

    
]