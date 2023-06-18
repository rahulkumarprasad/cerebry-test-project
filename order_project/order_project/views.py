from rest_framework import viewsets
from .serializer import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from .user_forms import UserCreateFrm
from django.contrib.auth.mixins import UserPassesTestMixin
from .product_form import ProductForm

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
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

class Login(View):
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

class Cart(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSer
    http_method_names = ['get', "post",'retrieve']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Cart, self).dispatch(*args, **kwargs)

class UserCreateView(View):
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
    def test_func(self):
        return self.request.user.is_superuser

class AdminProductAddView(SuperuserRequiredMixin,LoginRequiredMixin,View):
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
        print(request.POST,"\nfiles == ", request.FILES)
        if form.is_valid():
            new_user = form.save()
            form = ProductForm()
            context["form"] = form
        else:
            context["form"] = form
            return render(request, self.template, context)

        return render(request, self.template,context)

class AdminProductListView(SuperuserRequiredMixin,LoginRequiredMixin,View):
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
        print(request.POST,"\nfiles == ", request.FILES)
        if form.is_valid():
            new_user = form.save()
            form = ProductForm(instance = inst)
            context["form"] = form
        else:
            context["form"] = form
            return render(request, self.template, context)

        return render(request, self.template,context)


class AdminOrderView(SuperuserRequiredMixin,LoginRequiredMixin,View):
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