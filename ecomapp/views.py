from django.shortcuts import render
from .models import MenuList
from django.contrib.auth.decorators import login_required
from ecomapp.common_func import checkUserPermission
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from .views_payment import create_payment_request

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ecomapp.utils import generate_otp
from ecomapp.models import (
     MenuList,ProductMainCategory,Product,ProductSubCategory,Customer,OrderCart,Order,OrderDetail,EmailOTP
   
)

# Create your views here.


@login_required
def paginate_data(request, page_num, data_list):
    items_per_page, max_pages = 10, 10
    paginator = Paginator(data_list, items_per_page)
    last_page_number = paginator.num_pages

    try:
        data_list = paginator.page(page_num)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    current_page = data_list.number
    start_page = max(current_page - int(max_pages / 2), 1)
    end_page = start_page + max_pages

    if end_page > last_page_number:
        end_page = last_page_number + 1
        start_page = max(end_page - max_pages, 1)

    paginator_list = range(start_page, end_page)

    return data_list, paginator_list, last_page_number


@login_required
def setting_dashboard(request):
    get_setting_menu = MenuList.objects.filter(module_name='Setting', is_active=True)
   
    context = {
        "get_setting_menu": get_setting_menu,
        
    }
    return render(request, 'home/setting_dashboard.html', context)



@login_required 
def product_main_category_list_view(request):
    
    
    if not checkUserPermission(request, "can_view", "backend/product-main-category-list/"):
        return render(request,"403.html")

    product_main_categories = ProductMainCategory.objects.filter(is_active=True).order_by('-id')
    page_number = request.GET.get('page', 1)
    product_main_categories, paginator_list, last_page_number = paginate_data(request, page_number, product_main_categories)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'product_main_categories': product_main_categories,
    }

    return render(request, "product/main_category_list.html", context)  


@login_required
def add_product_main_category(request):
    if not checkUserPermission(request, "can_add", "backend/product-main-category-list/"):
        return render(request,"403.html")

    if request.method == 'POST':
        main_cat_name = request.POST.get('main_cat_name')
        cat_slug = request.POST.get('cat_slug')

        description = request.POST.get('description')
        
        product_main_category = ProductMainCategory(
            main_cat_name=main_cat_name,
            cat_slug=cat_slug,
            description=description,
            created_by=request.user
        )
        product_main_category.save()
        messages.success(request, 'Product Main Category added successfully.')
        return redirect('product_main_category_list')

    return render(request, 'product/add_product_main_category.html')


@login_required
def product_main_category_details(request, pk):
    if not checkUserPermission(request, "can_view", "backend/product-main-category-list/"):
        return render(request,"403.html")

    data = get_object_or_404(ProductMainCategory, pk=pk)
    
    context = {
        'data': data,
    }
    return render(request, 'product/product_main_category_details.html', context)

@login_required
def product_list(request):
    if not checkUserPermission(request, "can_view", "backend/product-list/"):
        return render(request,"403.html")

    products = Product.objects.filter(is_active=True).order_by('-id')
    page_number = request.GET.get('page', 1)
    products, paginator_list, last_page_number = paginate_data(request, page_number, products)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'products': products,
    }

    return render(request, "product/product_list.html", context)


@login_required
def product_detail(request, pk):
    if not checkUserPermission(request, "can_view", "backend/product-list/"):
        return render(request,"403.html")

    product = get_object_or_404(Product, pk=pk)
    
    context = {
        'product': product,
    }
    return render(request, 'product/product_detail.html', context)




@login_required
def add_new_product(request):
    if not checkUserPermission(request, "can_add", "backend/product-list/"):
        return render(request,"403.html")

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        discount_price = request.POST.get('discount_price')
        discount_percentage = request.POST.get('discount_percentage')
        description = request.POST.get('description')
        main_category_id = request.POST.get('main_category')
        sub_category_id = request.POST.get('sub_category')
        image = request.FILES.get('product_image')

        if not main_category_id or not sub_category_id or not product_name or not price or not stock:
            messages.error(request, 'All fields are required.')
            return redirect('add_new_product')
        main_category=ProductMainCategory.objects.filter(id=main_category_id, is_active=True).first()

        if not main_category:
            messages.error(request, 'Invalid main category selected.')
            return redirect('add_new_product')
        
        sub_category=ProductSubCategory.objects.filter(id=sub_category_id, is_active=True).first()

        if not sub_category:
            messages.error(request, 'Invalid Sub category selected.')
            return redirect('add_new_product')

        product = Product(
            product_name=product_name,
            product_image=image,
            price=price,
            stock=stock,
            discount_price=discount_price,
            discount_percentage=discount_percentage,
            description=description,
            main_category=main_category,
            sub_category=sub_category,
            created_by=request.user
        )
        product.save()
        
        messages.success(request, 'Product added successfully.')
        return redirect('product_list')

    main_categories= ProductMainCategory.objects.filter(is_active=True)
    sub_categories = ProductSubCategory.objects.filter(is_active=True)
    context = {
        'main_categories': main_categories,
        'sub_categories': sub_categories,
    }
    return render(request, 'product/add_new_product.html',context)


@login_required
def product_edit(request, pk):
    if not checkUserPermission(request, "can_update", "backend/product-list/"):
        return render(request,"403.html")

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        # product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.discount_percentage = request.POST.get('discount_percentage')
        product.main_category = get_object_or_404(ProductMainCategory, pk=request.POST.get('main_category'))
        product.sub_category = get_object_or_404(ProductSubCategory, pk=request.POST.get('sub_category'))
        product.updated_by = request.user
        product.save()
        
        messages.success(request, 'Product updated successfully.')
        return redirect('product_list')
    main_categories = ProductMainCategory.objects.filter(is_active=True)
    sub_categories = ProductSubCategory.objects.filter(is_active=True)
    context = {
        'product': product,
        'main_categories': main_categories,
        'sub_categories': sub_categories,
    }
    return render(request, 'product/product_edit.html', context)


def home(request):

    main_categories= ProductMainCategory.objects.filter(is_active=True)

    featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('-id')[:10]

    context = {
        'main_categories': main_categories,
        'featured_products': featured_products,
        
    }

    return render(request, 'website/home.html',context)


def login_view(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        
        profile = Customer.objects.get(phone=phone)
        user = authenticate(request, username=profile.user.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")

        next_url = request.GET.get('next')
        if next_url:
            next_url = next_url.strip()
        else:
            next_url = "home"
        return redirect(next_url)
            
        

    return render(request, 'website/user/login.html')




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['date_of_birth']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'website/user/register.html', {'error': 'Username already taken'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, phone=phone, date_of_birth=dob, is_active=False)
        messages.success(request,"registered successfully")

      


        generate_otp(email)

        return redirect(f'/backend/verify-otp/?email={email}')

    return render(request, 'website/user/register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')



def cart_amount_summary(request):

    sub_total_amount = 0
    total_vat = 0
    total_discount = 0
    grand_total = 0

    if request.user.is_authenticated:
        customer= Customer.objects.filter(user=request.user).first()
        cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)
        for item in cart_items:
            sub_total_amount += item.total_amount
            #total_vat += (item.product.price * 0.15)
    grand_total = (sub_total_amount + total_vat) - total_discount 

    return {'sub_total_amount': sub_total_amount, 'total_vat': total_vat, 'total_discount': total_discount, 'grand_total': grand_total}


#Products Details

def products_details(request, product_slug):

    product = Product.objects.filter(product_slug=product_slug, is_active=True).first()

    if not product:
        messages.error(request, "Product not found.")
        return redirect('home')
    
    if request.user.is_authenticated:
         customer = Customer.objects.filter(user=request.user).first()
         product_cart= OrderCart.objects.filter(customer=customer, product=product, is_active=True, is_order=False).first()
        
         if product_cart:
            product.product_cart = product_cart
    

    context = {
        'product': product,
    }
    return render(request, 'website/product/products_details.html', context)


def add_or_update_cart(request):

    
    is_authenticated = request.user.is_authenticated
    
    
    if is_authenticated:
        if request.method == 'POST':
            
            customer=Customer.objects.filter(user=request.user).first()
            
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 0))

            try:
                isRemoved = False

                cart_item, created = OrderCart.objects.update_or_create(
                    customer=customer, product_id=product_id, is_order=False, is_active=True,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    if quantity <= 0:
                        cart_item.is_active = False
                        isRemoved = True

                    cart_item.quantity = quantity
                    cart_item.save()

                amount_summary = cart_amount_summary(request)

                cart_item_count = OrderCart.objects.filter(customer=customer, is_order=False, is_active=True).count()
                print(f"Cart Item Count: {cart_item_count}")

               

                response = {
                    'status': 'success',
                    'message': 'Cart updated successfully',
                    'is_authenticated': is_authenticated,
                    'isRemoved': isRemoved,
                    'item_price': cart_item.total_amount,
                    'cart_item_count': cart_item_count,
                    'amount_summary': amount_summary,
                }
                
                return JsonResponse(response)
            

            except OrderCart.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Cart item not found', 'is_authenticated': is_authenticated,})

    return JsonResponse({'status': 'error', 'message': 'Invalid request', 'is_authenticated': is_authenticated,}, status=400)

@login_required
def cart(request):

    customer= Customer.objects.filter(user=request.user).first()
    context= {
        'customer': customer,

    }

    return render(request, 'website/cart/cart.html',context)  



@login_required
def checkout(request):

    amount_summary = cart_amount_summary(request)
    grand_total = amount_summary.get('grand_total', 0)

    if grand_total < 1:
        messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
        return redirect('cart')
    
    if request.method == 'POST':

        with transaction.atomic():

            billing_address = request.POST.get('billing_address')
            customer= Customer.objects.filter(user=request.user).first()

            if not billing_address:
                messages.error(request, "Billing address is required.")
                return redirect('checkout')
            
            cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)

            if len(cart_items) < 1:
                messages.error(request, "Your cart is empty. Please add items to your cart before proceeding to checkout.")
                return redirect('cart')
            else:

                order_obj= Order.objects.create(
                    customer=customer,
                    billing_address=billing_address,
                    
                )

                order_amount, shipping_charge, discount, coupon_discount, vat_amount, tax_amount = 0, 0, 0, 0, 0, 0

                for cart_item in cart_items:
                    order_amount += cart_item.total_amount

                    OrderDetail.objects.create(
                        order=order_obj,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.product.price,
                        total_price=cart_item.total_amount
                    )

                    grand_total = (order_amount + shipping_charge + vat_amount + tax_amount) - (discount + coupon_discount)

                    order_obj.order_amount = order_amount
                    order_obj.shipping_charge = shipping_charge
                    order_obj.discount = discount
                    order_obj.coupon_discount = coupon_discount
                    order_obj.vat_amount = vat_amount
                    order_obj.tax_amount = tax_amount
                    order_obj.due_amount = grand_total
                    order_obj.grand_total = grand_total
                    order_obj.save()

                    messages.success(request, "Order placed successfully.")

                    #print(f"Order Amount: {order_amount}, Shipping Charge: {shipping_charge}, Discount: {discount}, Coupon Discount: {coupon_discount}, VAT Amount: {vat_amount}, Tax Amount: {tax_amount}, Grand Total: {grand_total}")

                    response_data, response_status = create_payment_request(request, order_obj.id)
                    print(response_data)
                    print(response_status)

                    

                    if response_data['status'] == "SUCCESS":
                        for cart_item in cart_items:
                            cart_item.is_order = True
                            cart_item.save()

                        return redirect(response_data['GatewayPageURL'])
                    elif "error_message" in response_data:
                        messages.error(request, response_data['error_message'])
                    else:
                        messages.error(request, 'Failed to payment.')

                    

                    return redirect('home')

                        
                # Clear the cart after successful order placement


def request_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        generate_otp(email)
        return redirect(f'/backend/verify-otp/?email={email}')
    


def verify_otp_view(request):
    email = request.GET.get('email')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(email=email, code=otp).order_by('-created_at').first()

       

        if otp_obj and not otp_obj.is_expired():
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, "User not found. Please register first.")
                return redirect('register')
            customer = Customer.objects.filter(user=user).first()
            if customer:
                customer.is_active = True
                customer.save()
                messages.success(request, "OTP verified successfully. You can now log in.")
            else:
                messages.error(request, "Customer not found. Please contact support.")
            
            return redirect('home')
        else:
            messages.error(request, "Invalid or expired OTP.")

    return render(request, 'website/user/verify_otp.html', {'email': email})      

