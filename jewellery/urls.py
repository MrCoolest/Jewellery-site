# from django.contrib import admin
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView,  PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.loginUser,name='login'),
    path('logout',views.logoutUser,name='logout'),
    # path('forgot_passwd',views.forgot,name='forgot'),
    path('products',views.products,name='products'),
    path('necklaces',views.necklaces,name='necklace'),
    path('rings',views.rings,name='rings'),
    path('earings',views.earings,name='earings'),
    path('bangles',views.bangles,name='bangles'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('productView/<int:prod_id>',views.productView,name='productView'),

    path("password-reset/", 
    	PasswordResetView.as_view(template_name='forget_passwd.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
		name="password_reset_complete"),
    
  path('resend_otp',views.resend_otp),

  path('update_cart/',views.update_cart, name="update_cart"),


]