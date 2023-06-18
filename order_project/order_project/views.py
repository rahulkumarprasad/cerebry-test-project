from rest_framework import viewsets
from .serializer import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q, F, Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from .user_forms import UserCreateFrm, ShippingAddressForm
from django.contrib.auth.mixins import UserPassesTestMixin
from .product_form import ProductForm
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

class Home(View):
    '''This class is used for displaying information about products
    and implemented pagination and search feature
    '''
    template = "order/html/index.html"
    def get(self,request):
        search = request.GET.get("search",None)
        page = request.GET.get("page",1)
        start = (page-1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        products = Products.objects.all().order_by("name")
        if search != None:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        products = products[start:end]

        return render(request, self.template, {"title":"Home","products":products})

def user_logout(request):
    '''This function is used for logging-out the user'''
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

class Login(View):
    '''This class is used for logging user in the application'''
    template = "order/html/login.html"
    context = {"title":"Login"}
    def get(self,request):
        context = {}
        context.update(self.context)
    
        return render(request,self.template,context)

    def post(self,request):
        context = {}
        context.update(self.context)
        una = request.POST["username"]
        pas = request.POST["password"]
        user = authenticate(username=una, password=pas)
        if user is not None:
            red_url = request.GET.get("next",None)
            if red_url == None:
                red_url = "/"
            login(request,user)
            return redirect(red_url)
        else:
            context["error"]="Invalide crediential."
            return render(request,self.template,context)

class CartView(viewsets.ModelViewSet):
    '''Its a model viewset which is used for adding products to a user cart and updating it accordingly'''
    queryset = Cart.objects.all()
    serializer_class = CartSer
    http_method_names = ['get', "post",'retrieve',"delete"]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CartView, self).dispatch(*args, **kwargs)

class UserCreateView(View):
    '''It's a user create api for creating user'''
    template = "order/html/signup.html"
    
    def get(self,request):
        form = UserCreateFrm()
        return render(request,self.template,{"form":form})

    def post(self,request):
        form = UserCreateFrm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request,new_user)
            return redirect("/")
        else:
            return render(request, self.template, {'form': form})


class SuperuserRequiredMixin(UserPassesTestMixin):
    '''Its a class used for checking for a superuser and providing access'''
    def test_func(self):
        return self.request.user.is_superuser

class AdminProductAddView(SuperuserRequiredMixin,LoginRequiredMixin,View):
    '''this classe based api is used for admin to add new product'''
    template = "order/html/admin_pr_add.html"
    login_url = "/login"

    def get(self,request):
        context = {}
        form = ProductForm()
        context["form"] = form

        return render(request, self.template,context)

    def post(self,request):
        context = {}
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            form = ProductForm()
            context["form"] = form
        else:
            context["form"] = form
            return render(request, self.template, context)

        return render(request, self.template,context)

class AdminProductListView(SuperuserRequiredMixin,LoginRequiredMixin,View):
    '''This admin api will list all the products'''
    template = "order/html/admin_pr_list.html"
    login_url = "/login"

    def get(self,request):
        search = request.GET.get("search",None)
        page = request.GET.get("page",1)
        start = (page-1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        products = Products.objects.all().order_by("name")
        if search != None:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        products = products[start:end]

        return render(request, self.template, {"title":"Home","products":products})

class AdminProductUpdateView(SuperuserRequiredMixin,LoginRequiredMixin,View):
    '''This admin api is used for updating product detial'''
    template = "order/html/admin_pr_update.html"
    login_url = "/login"

    def get(self,request,id):
        context = {}
        inst = Products.objects.get(id=id)
        form = ProductForm(instance = inst)
        context["form"] = form

        return render(request, self.template,context)

    def post(self,request,id):
        context = {}
        inst = Products.objects.get(id=id)
        form = ProductForm(request.POST, request.FILES, instance = inst)
        if form.is_valid():
            new_user = form.save()
            form = ProductForm(instance = inst)
            context["form"] = form
        else:
            context["form"] = form
            return render(request, self.template, context)

        return render(request, self.template,context)


class AdminOrderView(SuperuserRequiredMixin,LoginRequiredMixin,View):
    '''This will show all the order placed by user's'''
    template = "order/html/admin_orders.html"
    login_url = "/login"

    def get(self,request):
        search = request.GET.get("search",None)
        page = request.GET.get("page",1)
        start = (page-1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        orders = Order.objects.select_related("user","shipping_address").all().order_by("-created_at")
        if search != None:
            orders = Order.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        orders = orders[start:end]

        return render(request, self.template, {"title":"Orders","orders":orders})


class AdminOrderUpdateView(SuperuserRequiredMixin,LoginRequiredMixin,View):
    '''This api is used for updating status of order'''
    template = "order/html/admin_order_update.html"
    login_url = "/login"

    def get(self,request,id):
        order = Order.objects.select_related("user","shipping_address").get(id=id)
        products_ordered = ProductOrdered.objects.select_related("product").filter(order=order)
        status = Order.STATUS_CHOICES
        return render(request, self.template, {"title":"Order-Update","order":order, "products_ordered":products_ordered,"status":status})

    def post(self,request,id):
        order = Order.objects.select_related("user","shipping_address").get(id=id)
        products_ordered = ProductOrdered.objects.select_related("product").filter(order=order)
        order.status = request.POST["status"]
        order.save()
        status = Order.STATUS_CHOICES
        return render(request, self.template, {"title":"Order-Update","order":order, "products_ordered":products_ordered,"status":status})

class ShippingCreateView(LoginRequiredMixin,View):
    '''This api is used for adding shipping address of customer'''
    template = "order/html/shipping.html"
    login_url = "/login"
    
    def get(self,request):
        form = ShippingAddressForm()
        return render(request,self.template,{"form":form})

    def post(self,request):
        form = ShippingAddressForm(request.POST,user = request.user)
        if form.is_valid():
            form.save()
            return redirect("/cart")
        else:
            return render(request, self.template, {'form': form})

class CartDetailsCount(APIView):
    '''This api is used for giving count of items in cart'''
    def get(self, request):
        try:
            cart_items = Cart.objects.get(user = request.user).product_added.all()
            count = cart_items.count()
            return Response({"cart_count":count})
        except:
            return Response({},status=500)

class CartListView(LoginRequiredMixin,View):
    '''This api is used for viewing cart and placing order and also selecting payment mode and shipping address'''
    template = "order/html/cart_list.html"
    login_url = "/login"
    
    def get_context_data(self,request):
        try:
            cart_details = Cart.objects.prefetch_related("product_added").get(user=request.user)
            total = cart_details.product_added.all().select_related("product").annotate(total_price = (F("quantity")* F("product__price")))
            sub_total = total.aggregate(Sum("total_price"))["total_price__sum"]
        except Cart.DoesNotExist as e:
            logging.error(f"Error occured, message {e}")
            cart_details = None
            total = []
            sub_total = 0
        payment_method = ["COD","Online"]
        shipping_addr_list = ShippingAddress.objects.filter(user = request.user)
        return {"cart_details":None,"shipping_addr_list":shipping_addr_list, 
                "total_amount":sub_total,"product_detail":total,"payment_method":payment_method}

    def get(self,request):
        context = {}
        context = self.get_context_data(request)
        return render(request,self.template,context)
    
    def post(self,request):
        context = {}
        try:
            cart_details = Cart.objects.prefetch_related("product_added").get(user=request.user)
            shipping = ShippingAddress.objects.get(id=request.POST["shipping"])
            products_in_cart = cart_details.product_added.all().select_related("product")
            total_amount = 0
            bulk_create_lst = []
            odr = Order(user=request.user, shipping_address = shipping, status="PENDING",
            total_amount = total_amount, payment_type = request.POST["payment_type"])
            for pr_cart in products_in_cart:
                pr_price = pr_cart.quantity * pr_cart.product.price
                total_amount += pr_price
                bulk_create_lst.append(ProductOrdered(order=odr,product=pr_cart.product,
                quantity=pr_cart.quantity, price=pr_cart.product.price))
            
            odr.total_amount = total_amount
            odr.save()
            ProductOrdered.objects.bulk_create(bulk_create_lst)
            cart_details.delete()
            return redirect("/order/list")
        except Cart.DoesNotExist as e:
            logging.error(f"Error occured, message {e}")

        context = self.get_context_data(request)
        return render(request,self.template,context)

class OrderListView(LoginRequiredMixin,View):
    '''This api is used for displaying all order of a user'''
    template = "order/html/order_list.html"
    login_url = "/login"

    def get(self,request):
        context = {}
        context["orders"] = Order.objects.select_related("shipping_address").filter(
            user=request.user).annotate(count = Count(F("productordered"))).order_by("-created_at")
        return render(request,self.template,context)

class OrderDetailsView(LoginRequiredMixin,View):
    '''This api is used for displaying order details of a user'''
    template = "order/html/order_details.html"
    login_url = "/login"

    def get(self,request,id):
        try:
            context = {}
            order = Order.objects.select_related("shipping_address").get(id=id,user=request.user)
            products_ordered = ProductOrdered.objects.select_related("product").annotate(total_price = (F("quantity")* F("product__price"))).filter(order=order)
            context["order"] = order
            context["products_ordered"] = products_ordered
            return render(request,self.template,context)

        except:
            return redirect("/order/list")