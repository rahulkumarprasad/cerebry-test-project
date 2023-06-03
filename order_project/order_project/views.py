from rest_framework import viewsets
from .serializer import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', "put", "post",'retrieve']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(OrderView, self).dispatch(*args, **kwargs)