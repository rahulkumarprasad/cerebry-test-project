from django.db import models
from django.contrib.auth.models import User

def product_directory(instance,filename):
    return f"products/{str(instance.name).replace(' ','_')}/{str(filename).replace(' ','_')}"

class Products(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = product_directory)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.user.username

class ProductCart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.product.name}"

class Cart(models.Model):
    '''This is used to store info into user cart'''
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_added = models.ManyToManyField(ProductCart)
    checked_out = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.user.username}: {self.product_added.all().count()}"



class Order(models.Model):
    '''This is used to store order info of user'''
    STATUS_CHOICES = (("PENDING","PENDING"), ("SHIPPED","SHIPPED"), ("DELIVERED","DELIVERED"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)
    status = models.CharField(max_length = 9,choices = STATUS_CHOICES,default="PENDING")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user.username}: {self.status}"

class ProductOrdered(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.order.user.username}"