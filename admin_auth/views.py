from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from user_auth.models import CustomUserManager, CustomUser
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
# Create your views here.

# Admin login login working pending session management


def admin_login(request):
    if 'email' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            if CustomUser.objects.filter(email=email).exists():
                user_obj = CustomUser.objects.get(email=email,is_superuser=True)
                if user_obj.check_password(password):  # Use check_password to verify password
                    login(request, user_obj)
                    request.session['email']=email
                    return redirect('dashboard/')
                else:
                    messages.error(request,"Incorrect password")
            else:
                messages.error('User not found')
            
        return render(request,'admin_auth/authentication-login.html')
    
#______________________________________________________________dashboard view _______________________________________pending work session managemnet login required
@login_required
def dashboard(request):
    if 'email' in request.session:
        return render(request,'admin_auth/index.html')
    return redirect('admin_login')

# ----------------------------------------------------------------User_manaagement---------------------------------pending work session management
@login_required
def User_management(request):
    if 'email' in request.session:
     user=CustomUser.objects.filter(is_superuser=False)
    
     context={
         'user':user,
     }
     return render(request,'admin_auth/usermanagement.html',context)
    return render(request,'admin_auth/authentication-login.html')

# ----------------------------------------------------------------block------------------------------all working url parameters 
@login_required
def block(request,user_id):
    if 'email' in request.session:
        user=CustomUser.objects.get(id=user_id)
        user.is_active=False
        user.save()
    
        return redirect('user_management')
    return render(request,'admin_auth/authentication-login.html')
#----------------------------------------------------------------unblock--------------------------------aLLL WORKINGH URL MANAMNGEMNET
@login_required
def unblock(request,user_id):
    if 'email' in request.session:
        user=CustomUser.objects.get(id=user_id)
        user.is_active=True
        user.save()
    
        return redirect('user_management')
    return render(request,'admin_auth/authentication-login.html')

@login_required
def delete_user(request,id):
    if 'email' in request.session:
     user=CustomUser.objects.get(id=id)
     user.delete()
     return redirect('user_management')


# ------------------------------------------------------------------user view details ---------------------------------login required-----
def userviewdetails(request,user_id):
    if 'email' in request.session:
        user=CustomUser.objects.get(id=user_id)
        context={
        'user':user,
        }
        return render(request, 'admin_auth/userviewdetails.html',context)
    
    

def admin_logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect('admin_login')