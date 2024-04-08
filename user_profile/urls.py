from django.contrib import admin
from django.urls import path,include
from admin_auth import views
from django.conf import settings
from django.conf.urls.static import static
from admin_auth import views
from user_auth import views
from user_profile import views

urlpatterns = [
    path('user_acc/',views.account_page,name='account'),
    path('profile_management/', views.manage_profile, name='user_profile_management'),
    path('manage_address/', views.manage_address, name='manage_address'),
    path('edit_address/<int:address_id>/', views.address_edit, name='edit_address'),
    path('view_address/<int:address_id>/',views.view_address, name='view_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('orders_page/',views.order_page,name='orders_page'),
    # path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.show_cart, name='show_cart'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_orders/', views.confirm_orders, name='confirm_orders'),
    path('wallet_payment/<int:order_id>/', views.wallet_payment, name='wallet_payment'),
    path('orders/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cart-items-count/', views.cart_items_count, name='cart_items_count'),
    path('track-order/', views.track_order, name='track_order'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('wishlist_view/', views.wishlist, name='wishlist'),
    path('user_wishlist/', views.user_add_to_wishlist, name='add_to_user_wishlist'),
    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('success/',views.success,name="success"),
    path('razor_pay/',views.razor_payment,name="razor_payment"),
    path('change_password/',views.reset_password,name="reset_passwords"),
    

]