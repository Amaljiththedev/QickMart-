from django.shortcuts import redirect, render
from .models import *
from admin_auth import views 

# Create your views here.


def category_list(request):
    
    cat=category.objects.all()
    
    context={
        'cat':cat,
    }
    return render(request, 'admin_auth/category.html', context)
    
    
def add_category(request):
    
    
    if request.method == 'POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image = request.FILES.get('image')
        category_offer_description=request.POST.get('category_offer_description')
        category_offer=request.POST.get('category_offer')
    
        new_category=category(
            name=name,
            description=description,
            image=image,
            category_offer_description=category_offer_description,
            category_offer=category_offer
        )
    
        new_category.save()
        return redirect('category')
    return render(request, 'admin_auth/add_category.html')
    
    
def delete_category(request,id):
    cat=category.objects.get(id=id)
    cat.delete()
    return redirect('category')
    


def edit_category(request,id):
    
    cat=category.objects.get(id=id)
    if request.method=='POST':
            name=request.POST.get('name')
            description=request.POST.get('description')
            image = request.FILES.get('image')
            category_offer_description=request.POST.get('category_offer_description')
            category_offer=request.POST.get('category_offer')
            
            
            
            cat.name=name
            cat.description=description
            cat.category_offer=category_offer
            cat.image=image
            cat.category_offer_description=category_offer_description  
            cat.save() 
          
            
            return redirect('category')
            
    context={
            'cat':cat,
            }    
        
    return render(request, 'admin_auth/edit_category.html',context)



def block_category(request,id):
    cat=category.objects.get(id=id)
    cat.is_active=False
    cat.save()
    
    return redirect('category')
    
def unblock_category(request,id):
    cat=category.objects.get(id=id)
    cat.is_active=True
    cat.save()
    
    return redirect('category')

def add_brand(request):
    
    if request.method == 'POST':
        brand=request.POST.get('brand')
        logo=request.FILES.get('logo')
        
        new_brand=Brand.objects.create(brand_name=brand,logo=logo)
        return redirect('category')
    
    return render(request, 'admin_auth/add_brand.html')