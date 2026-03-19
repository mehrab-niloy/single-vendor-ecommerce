from django.contrib import admin
from .models import ( ProductMainCategory,ProductSubCategory,Product,OrderCart)
@admin.register(ProductMainCategory)
class ProductMainCategoryAdmin(admin.ModelAdmin):
    list_display         = ('main_cat_name', 'cat_slug', 'cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('main_cat_name', 'cat_slug')
    ordering             = ('cat_ordering',) 


@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display         = ('sub_cat_name', 'main_category', 'sub_cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('sub_cat_name', 'sub_cat_slug')
    ordering             = ('sub_cat_ordering',)

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display         = ('product_name', 'main_category', 'sub_category','price','stock', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active','main_category', 'sub_category')
    search_fields        = ('product_name', 'main_category__main_cat_name', 'sub_category__sub_cat_name', 'product_slug')
    ordering             = ('product_name',) 

admin.site.register(OrderCart)
