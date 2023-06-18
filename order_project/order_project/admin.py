from django.contrib import admin
from .models import *

#registering all models for showing in admin pannel
admin.site.register([Order,Products, ShippingAddress, Cart, ProductOrdered, ProductCart])