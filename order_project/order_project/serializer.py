from rest_framework import serializers
from .models import *
from django.db.models import F, Q

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['id','name', 'quantity', 'price']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     class Meta:
#         model = Order
#         fields = "__all__"
    
#     def create(self,validated_data):
#         items = validated_data.pop("items")
#         odr = Order.objects.create(**validated_data)
#         for item in items:
#             itm_obj = OrderItem.objects.create(order=odr,**item)
#         return odr
    
#     def update(self, instance, validated_data):
#         instance.status = validated_data.get('status', instance.status) 
#         instance.save()
#         return instance

class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','image','name','description', 'price']

class ProductCartSer(serializers.ModelSerializer):
    product = ProductSer()
    class Meta:
        model = ProductCart
        fields = ['product','quantity']

class CartSer(serializers.ModelSerializer):
    product_added = ProductCartSer(many=True)
    class Meta:
        model = Cart
        fields = ['user','product_added', 'checked_out']

 