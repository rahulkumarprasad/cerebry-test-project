from rest_framework import viewsets
from .serializer import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render

class Home(View):
    template = "order/html/index.html"
    
    def get(self,request):
        return render(request, self.template, {"title":"Home"})

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    #serializer_class = OrderSerializer
    http_method_names = ['get', "put", "post",'retrieve']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(OrderView, self).dispatch(*args, **kwargs)

class Cart(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSer
    http_method_names = ['get', "put", "post",'retrieve']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Cart, self).dispatch(*args, **kwargs)