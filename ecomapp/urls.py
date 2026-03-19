from django.urls import path
from . import views,views_payment

urlpatterns = [
     path('dashboard/', views.setting_dashboard, name='dashboard'),
     path('setting-dashboard/',views.setting_dashboard,name='setting_dashboard'),
     path('product-main-category-list/',views.product_main_category_list_view,name='product_main_category_list'),
     path('add-product-main-category/',views.add_product_main_category,name='add_product_main_category'),
     path('product-main-category/<int:pk>/', views.product_main_category_details, name='product_main_category_details'),
     path('product-list/',views.product_list,name='product_list'),
     path('product/<int:pk>/', views.product_detail, name='product_detail'),
     path('product-create/', views.add_new_product, name='add_new_product'),
    path('product/edit/<int:pk>/', views.product_edit, name='edit_product'),
    path('products/<slug:product_slug>/', views.products_details, name='products_details'),

       path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('request-otp/', views.request_otp_view, name='request_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),


     #ajax

    path('add-or-update-cart/', views.add_or_update_cart, name='add_or_update_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),


     
    #Payment

    path('payment/success/<str:str_data>/', views_payment.payment_complete, name='payment_complete'),
    path('payment/cancel/<str:str_data>/', views_payment.payment_cancel, name='payment_cancel'),
    path('payment/failed/<str:str_data>/', views_payment.payment_failed, name='payment_failed'),
    path('payment/check/<str:str_data>/', views_payment.payment_check, name="payment_check"),




]

