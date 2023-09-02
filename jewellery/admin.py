from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)  
admin.site.register(Contact_Form)  