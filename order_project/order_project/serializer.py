from rest_framework import serializers
from .models import *
from django.db.models import F, Q

class ProductSer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Products
        fields = ['id','image','name','description', 'price']
        read_only_fields = ('image', 'name', 'description', 'price')

class ProductCartSer(serializers.ModelSerializer):
    product = ProductSer()
    class Meta:
        model = ProductCart
        fields = ['product','quantity']

class CartSer(serializers.ModelSerializer):
    '''Serializer for DRF for card data'''
    product_added = ProductCartSer(many=True)
    class Meta:
        model = Cart
        fields = ['id','product_added', 'checked_out']
        
    def create(self,validated_data):
        request = self.context['request']
        user = request.user

        products_lst = validated_data.pop("product_added")

        try:
            cart = Cart.objects.get(user=user)
        except:
            cart = Cart.objects.create(user=user)

        product_mapper_dict_with_quantity = {}
        cart_product_list = []
      
        already_product = cart.product_added.all()
        ids_traversed = []
        
        for pr in already_product:
            product_mapper_dict_with_quantity[pr.product.id] = {"pr_cart_obj":pr}
            cart_product_list.append(pr)
            ids_traversed.append(pr.product.id)

        pr_ids_to_get = []
        for products in products_lst:
            if int(products["product"]["id"]) not in ids_traversed:
                pr_ids_to_get.append(products["product"]["id"])
                product_mapper_dict_with_quantity[int(products["product"]["id"])] = {"quantity": products["quantity"]}
                
            else:
                temp_pr_cart_obj = product_mapper_dict_with_quantity[int(products["product"]["id"])]["pr_cart_obj"]
                if products["quantity"] == 0:
                    cart_product_list.remove(temp_pr_cart_obj)
                    temp_pr_cart_obj.delete()
                elif products["quantity"] < 0 and (temp_pr_cart_obj.quantity + products["quantity"]) <= 0:
                    cart_product_list.remove(temp_pr_cart_obj)
                    temp_pr_cart_obj.delete()
                elif products["quantity"] < 0:
                    temp_pr_cart_obj.quantity += products["quantity"]
                else:
                    temp_pr_cart_obj.quantity += products["quantity"]


        ProductCart.objects.bulk_update(cart_product_list,fields=["quantity"])

        if len(pr_ids_to_get) != 0:

            products_objs = Products.objects.filter(id__in = pr_ids_to_get)
            for pr in products_objs:
                temp_obj = ProductCart(product=pr,quantity=product_mapper_dict_with_quantity[pr.id]["quantity"])
                temp_obj.save()
                cart_product_list.append(temp_obj)
        
        cart.product_added.set(cart_product_list)
        cart.save()

        return cart