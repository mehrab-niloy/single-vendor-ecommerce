from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime
from django.utils import timezone


# Create your models here.
class MenuList(models.Model):
    module_name        = models.CharField(max_length=100, db_index=True)
    menu_name          = models.CharField(max_length=100, unique=True, db_index=True)
    menu_url           = models.CharField(max_length=250, unique=True)
    menu_icon          = models.CharField(max_length=250, blank=True, null=True)
    parent_id          = models.IntegerField()
    is_main_menu       = models.BooleanField(default=False)
    is_sub_menu        = models.BooleanField(default=False)
    is_sub_child_menu  = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(blank=True, null=True)
    deleted_at         = models.DateTimeField(blank=True, null=True)
    created_by         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active          = models.BooleanField(default=True)
    deleted            = models.BooleanField(default=False)

    class Meta:
        db_table = "menu_list"

    def __str__(self) -> str:
        return self.menu_name

class UserPermission(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user_for_permission") 
    menu          = models.ForeignKey(MenuList, on_delete=models.CASCADE, related_name="menu_for_permission") 
    can_view      = models.BooleanField(default=False)
    can_add       = models.BooleanField(default=False)
    can_update    = models.BooleanField(default=False)
    can_delete    = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user") 
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by_user", blank=True, null=True) 
    deleted_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deleted_by_user", blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    deleted       = models.BooleanField(default=False)

    class Meta:
        db_table = "user_permission"

    def __str__(self):
        return str(self.menu)




class ProductMainCategory(models.Model):
    main_cat_name = models.CharField(max_length=100, unique=True)
    cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    cat_image     = models.ImageField(upload_to='ecommerce/category_images/', blank=True, null=True)
    description   = models.TextField(blank=True, null=True)
    cat_ordering  = models.IntegerField(default=0,blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'
        verbose_name_plural = 'Product Categories'
        ordering = ['-is_active','cat_ordering']

    def __str__(self):
        return self.main_cat_name
    
     
    
    def save(self, *args, **kwargs):
        if not self.cat_slug and self.main_cat_name:
            base_slug = slugify(self.main_cat_name)
            slug = base_slug
            num = 1
            while ProductMainCategory.objects.filter(cat_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.cat_slug = slug
        super().save(*args, **kwargs)
    
    

class ProductSubCategory(models.Model):
    main_category = models.ForeignKey(ProductMainCategory, on_delete=models.CASCADE, related_name='sub_categories', null=True,
    blank=True)
    sub_cat_name = models.CharField(max_length=100, unique=True)
    sub_cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    sub_cat_image     = models.ImageField(upload_to='ecommerce/category_images/', blank=True, null=True)
    description   = models.TextField(blank=True, null=True)
    sub_cat_ordering  = models.IntegerField(default=0,blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)


    class Meta:
        db_table = 'product_sub_category'
        verbose_name_plural = 'Product Sub Categories'
        ordering = ['-is_active','sub_cat_ordering']

    def __str__(self):
        return self.sub_cat_name
    
    def save(self, *args, **kwargs):
        if not self.sub_cat_slug and self.sub_cat_name:
            base_slug = slugify(self.sub_cat_name)
            slug = base_slug
            num = 1
            while ProductSubCategory.objects.filter(sub_cat_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.sub_cat_slug = slug
        super().save(*args, **kwargs)

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    product_slug = models.SlugField(max_length=150, unique=True, blank=True)
    product_image = models.ImageField(upload_to='ecommerce/product_images/', blank=True, null=True)
    main_category = models.ForeignKey(ProductMainCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    total_views = models.PositiveIntegerField(default=0)
    discount_percentage = models.PositiveIntegerField(default=0, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_updated_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'Products'
        ordering = ['-is_active']

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.product_slug and self.product_name:
            base_slug = slugify(self.product_name)
            slug = base_slug
            num = 1
            while Product.objects.filter(product_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.product_slug = slug
        super().save(*args, **kwargs)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class OrderCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_order= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return_value=float(self.quantity) * float(self.product.price)
        return return_value
    
    class Meta:
        db_table = 'order_cart'

    def __str__(self):
        return f"{self.customer} - {self.product.product_name} ({self.quantity})"



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    billing_address = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    order_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    shipping_charge = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    coupon_discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    vat_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    due_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    grand_total = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_number)+" ("+str(self.customer)+" - "+str(self.created_at)+")"

    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        if not self.order_number:
            current_year = datetime.date.today().year
            current_month = datetime.date.today().month
            current_day = datetime.date.today().day
            current_customer_id = self.customer.id

            last_order = Order.objects.filter(order_number__startswith=f"{current_year}{current_month:02d}")

            increase_number = 1
            new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"

            while Order.objects.filter(order_number=new_order_number).exists():
                increase_number += 1
                new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"

            self.order_number = new_order_number

        super().save(*args, **kwargs)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.product)+" - "+str(self.quantity)+")"

    class Meta:
        db_table = 'order_details'



class OnlinePaymentRequest(models.Model):
    order = models.ForeignKey(Order, related_name='order_payment_requests', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status_list = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Failed', 'Failed')]
    payment_status = models.CharField(max_length=15, choices=payment_status_list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_request_created_by')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "online_payment_request"



class OrderPayment(models.Model):
    order = models.ForeignKey(Order, related_name='order_payments', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.payment_method)+" - "+str(self.amount)+")"

    class Meta:
        db_table = 'order_payments'


#Email OTP Verification

class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=60)

    def __str__(self):
        return f"{self.email} - {self.code}"
    


    



