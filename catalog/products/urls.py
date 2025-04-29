"""
URL configuration for catalog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from .views import index, product_details, cart_add, cart_detail_view, checkout


app_name = "products"

urlpatterns = [
    path("", index, name="index"),
    path("product/<int:product_id>/", product_details, name="product_details"),
    path("checkout/", checkout, name="checkout"),
    path("cart_add/<int:product_id>", cart_add, name="cart_add"),
    path("cart_detail/", cart_detail_view, name="cart_detail"),
]
