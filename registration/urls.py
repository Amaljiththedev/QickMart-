from django.contrib import admin
from django.urls import path,include
from admin_auth import views
from django.conf import settings
from django.conf.urls.static import static
from admin_auth import views
from registration import views
from reset_password import views as reset_password
urlpatterns = [
    path('login/', views.user_login,name='login'),
    path('register/', views.register,name='register'),
    path('otp/', views.verify_otp,name='otp'),
    path('logout_view/', views.logout_view,name='logout_view'),
    path('cancel/', views.cancel_view,name='cancel'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_reset_otp/', reset_password.verify_otp, name='verify_reset_otp'),
    path('forget_password/', reset_password.forgot_password, name='forget_password'),
    path('change_password/',reset_password.change_password,name='change_password')

    
]