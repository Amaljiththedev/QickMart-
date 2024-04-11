"""
URL configuration for Qickmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from admin_auth import views
from django.conf import settings
from django.conf.urls.static import static
from admin_auth import views
from user_auth import views
from user_profile import views as account
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('admin_auth.urls')),
    path('',views.home, name='home'),
    path('base', views.base, name='base'),
    path('register/', include('registration.urls')),
    path('user_auth/', include(('user_auth.urls', 'user_auth'), namespace='user_auth')),
    path('user_profile/',include(('user_profile.urls', 'user_profile'),namespace='user_profile')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
