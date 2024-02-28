from django.shortcuts import redirect, render
from .models import Products,Product_images
from category.models import category as Category  # Import the Category model
from category.models import Brand as Brand
from admin_auth import views


# Create your views here.
def product_view(request):
    products=Products.objects.all()
    
    context={
        'products': products
    }
    return render(request, 'admin_auth/product_management.html',context)

def add_product(request):
    
    status_choices=Products.Status_choices
    categories = Category.objects.all()
    brand= Brand.objects.all()


    
    context={
        'categories': categories,
        'status_choices':status_choices,
        'brand':brand,
    }
    if request.method=='POST':
        title=request.POST.get('title')
        cat_id=request.POST.get('category')
        description=request.POST.get('description')
        price=request.POST.get('price')
        brand_id=request.POST.get('brand')
        status=request.POST.get('status')
        stock_count=request.POST.get('stock_count')
        image=request.FILES.get('image')
        sku=request.POST.get('sku')
        weight=request.POST.get('weight')
        dimensions=request.POST.get('dimensions')
        available = request.POST.get('available') == 'on'
        featured = request.POST.get('featured') == 'on'
        product_image1=request.FILES.get('product_image1')
        product_image2=request.FILES.get('product_image2')
        product_image3=request.FILES.get('product_image3')
        product_image4=request.FILES.get('product_image4')
        product_image5=request.FILES.get('product_image5')
        print(brand_id)
        print(brand_id)
        
        
        
        brand=Brand.objects.get(id=brand_id)
        cat=Category.objects.get(id=cat_id)
        item=Products.objects.create(
            title=title,
            category=cat,
            description=description,
            price=price,
            brand=brand,
            status=status,
            stock_count=stock_count,
            image=image,
            sku=sku,
            weight=weight,
            dimensions=dimensions,
            available=available,
            featured=featured,
            )
        if product_image1:
            Product_images.objects.create(product=item, product_image1=product_image1)
        if product_image2:
            Product_images.objects.create(product=item, product_image2=product_image2)
        if product_image3:
            Product_images.objects.create(product=item, product_image3=product_image3)
        if product_image4:
            Product_images.objects.create(product=item, product_image4=product_image4)
        if product_image5:
            Product_images.objects.create(product=item,product_image5=product_image5)
            # creating product image instance for storing product image that is a foreign key of product
            
            
        return redirect('product_management')
        
    return render(request, 'admin_auth/product_add.html',context)



def update_product(request, id):
    product = Products.objects.get(id=id)
    status_choices = Products.Status_choices
    categories = Category.objects.all()
    product_images = Product_images.objects.filter(product=product)
    brand=Brand.objects.all()

    context = {
        'brand': brand,
        'categories': categories,
        'status_choices': status_choices,
        'product': product,
        'product_images': product_images
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        cat_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand_id = request.POST.get('brand')
        stock_count = request.POST.get('stock_count')
        image = request.FILES.get('image')
        sku = request.POST.get('sku')
        weight = request.POST.get('weight')
        dimensions = request.POST.get('dimensions')
        available = request.POST.get('available') == 'on'
        featured = request.POST.get('featured') == 'on'
        product_image1 = request.FILES.get('product_image1')
        product_image2 = request.FILES.get('product_image2')
        product_image3 = request.FILES.get('product_image3')
        product_image4 = request.FILES.get('product_image4')
        product_image5 = request.FILES.get('product_image5')

        # Update product fields
        product.title = title
        product.category = Category.objects.get(id=cat_id)
        product.description = description
        product.price = price
        product.brand = Brand.objects.get(id=brand_id)
        product.stock_count = stock_count  
        product.image = image
        product.sku = sku
        product.weight = weight
        product.dimensions = dimensions
        product.available = available        
        product.featured = featured
        
        # Handle product images
        if product_image1:
            Product_images.objects.create(product=product, product_image1=product_image1)
        if product_image2:
            Product_images.objects.create(product=product, product_image2=product_image2)
        if product_image3:
            Product_images.objects.create(product=product, product_image3=product_image3)
        if product_image4:
            Product_images.objects.create(product=product, product_image4=product_image4)
        if product_image5:
            Product_images.objects.create(product=product,product_image5=product_image5)
        product.save()

        return redirect('product_management')

    return render(request, 'admin_auth/product_update.html', context)


def block_product(request,id):
    product=Products.objects.get(id=id)
    product.is_active=False
    product.save()
    print("block")
    return redirect('product_management')



def unblock_product(request,id):
    product=Products.objects.get(id=id)
    product.is_active=True
    product.save()
    print(product.is_active)
    return redirect('product_management')
    
def delete_product(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    return redirect('product_management')