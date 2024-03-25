from django.shortcuts import render
from category.models import category,Brand
from banner.models import Banner
from category.views import views
from products.models import ProductVariant, Products, ProductImage

# Create your views here.
def base(request):
    return render(request, 'user_auth/base.html')

def home(request):
    print("This is printing from home page")
    Category=category.objects.filter(is_active=True)[:5]
    products=Products.objects.filter(is_active=True,status='In Stock')
    brand=Brand.objects.all()


    
    
    
    context={
        'Category': Category,
        'products': products,
        'brand': brand,
    }
    
    
    return render(request,'user_auth/main.html',context)

def user_product_view(request, id):
    product = Products.objects.get(id=id)
    product_images =ProductImage.objects.filter(product=product)
    variants = ProductVariant.objects.filter(product=product)

    context = {
        'product_images': product_images,
        'product': product,
        'variants': variants,
    }

    return render(request, 'user_auth/product-view.html', context)

def banner_view(request):
    laptop_banner=category.objects.get(name='Laptop')
    Tvandbanner=category.objects.get(name='Tv and audio')
    smartphonebanner=category.objects.get(name='smartphone')
    wearablesbanner=category.objects.get(name='Wearables')
    
    allban=Banner.objects.filter(is_active=True)
    lapban=Banner.objects.filter(category=laptop_banner,is_active=True)       
    tvban=Banner.objects.filter(category=Tvandbanner,is_active=True)
    smartphoneban=Banner.objects.filter(category=smartphonebanner,is_active=True)
    wearablesbanner=Banner.objects.filter(category=wearablesbanner,is_active=True)
    
    context={
        'allban':allban,
        'lapban':lapban,
        'tvban':tvban,
        'wearablesbanner':wearablesbanner,
        'smartphoneban':smartphoneban, 
        
    }
    
    return render(request, 'user_auth/product-view.html', context)        



def list_of_products(request):
    products = Products.objects.filter(is_active=True)
    categories = category.objects.all()
    brands = Brand.objects.all()
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if category_id:
        products = products.filter(category_id=category_id)
    elif brand_id:
        products = products.filter(brand_id=brand_id)
    elif sort_by:
        if sort_by == 'sales_asc':
            products = products.order_by('title')  # Sort by product name ascending
        elif sort_by == 'sales_desc':
            products = products.order_by('-title')  # Sort by product name descending
        elif sort_by == 'price_asc':
            products = products.order_by('price')  # Sort by price ascending
        elif sort_by == 'rating_asc':
            products = products.order_by('rating')  # Sort by rating ascending
        elif sort_by == 'date_desc':
            products = products.order_by('-created_date')  # Sort by creation date descending
            
        elif sort_by =='trending':
            products = products.filter(trending=True)
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'sort_by': sort_by,  # Pass the current sorting parameter to the template
    }

    return render(request, 'user_auth/product_list.html', context)