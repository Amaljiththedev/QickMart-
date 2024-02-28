from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from user_auth.models import CustomUserManager, CustomUser
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

# Admin login login working pending session management



def admin_login(request):
        if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            if CustomUser.objects.filter(email=email).exists():
                user_obj = CustomUser.objects.get(email=email)
                if user_obj.check_password(password):  # Use check_password to verify password
                    login(request, user_obj)
                    return redirect('dashboard/')
                else:
                    messages.error(request,"Incorrect password")
            else:
                messages.error('User not found')
            
        return render(request,'admin_auth/authentication-login.html')
    
#______________________________________________________________dashboard view _______________________________________pending work session managemnet login required
def dashboard(request):
    return render(request,'admin_auth/index.html')

# ----------------------------------------------------------------User_manaagement---------------------------------pending work session management
def User_management(request):
    user=CustomUser.objects.filter(is_superuser=False)
    
    context={
        'user':user,
    }
    return render(request,'admin_auth/usermanagement.html',context)


# ----------------------------------------------------------------block------------------------------all working url parameters 
def block(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    
    user.is_active=False
    user.save()
    return redirect('user_management')
#----------------------------------------------------------------unblock--------------------------------aLLL WORKINGH URL MANAMNGEMNET
def unblock(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    
    user.is_active=True
    user.save()
    return redirect('user_management')


# ------------------------------------------------------------------user view details ---------------------------------login required-----
def userviewdetails(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    
    context={
        'user':user,
    }
    
    return render(request, 'admin_auth/userviewdetails.html',context)


def admin_logout(request):
    logout(request)
    return redirect('home')