from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name="shopHome"),
    path('about/', views.about,name="AboutUS"),
    path('contact/', views.contact,name="ContactUS"),
    path('tracker/', views.tracker,name="tracker"),
    path('search/', views.search,name="search"),
    path('products/<int:myid>', views.product,name="productview"),
    path('checkout/', views.checkout,name="checkout"),

]