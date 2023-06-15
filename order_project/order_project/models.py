from django.db import models
from django.contrib.auth.models import User

def product_directory(instance,filename):
    return f"products/{instance.name}/{filename}"

class Products(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = product_directory)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

class Order(models.Model):
    STATUS_CHOICES = (("PENDING","PENDING"), ("SHIPPED","SHIPPED"), ("DELIVERED","DELIVERED"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)
    status = models.CharField(max_length = 9,choices = STATUS_CHOICES,default="PENDING")
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

    
