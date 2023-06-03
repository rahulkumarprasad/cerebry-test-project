from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = (("PENDING","PENDING"), ("SHIPPED","SHIPPED"), ("DELIVERED","DELIVERED"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length = 9,choices = STATUS_CHOICES,default="PENDING")
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True, related_name='items')
    name = models.CharField(max_length = 200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add= True)