"""order_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from . import views as vw
from rest_framework import routers, urls as r_urls
from django.conf.urls import url

router = routers.DefaultRouter()
#router.register(r"",vw.OrderView)
router.register(r"cart",vw.Cart)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vw.Home.as_view() ,name="home"),
    path("api/",include(router.urls)),
    path('auth/', include(r_urls, namespace='rest_framework')),
    path("logout",vw.user_logout,name="logout"),
    path("login",vw.Login.as_view(), name="login"),
    path("signup",vw.UserCreateView.as_view(), name="signup"),
    path("products/add",vw.AdminProductAddView.as_view(), name="admin_view"),
    path("products/update",vw.AdminProductListView.as_view(), name="admin_product_list"),
    path("products/update/<int:id>",vw.AdminProductUpdateView.as_view(), name="admin_product_update"),
    path("products/orders",vw.AdminOrderView.as_view(), name="admin_order_view"),

    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}), 
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT})

]
