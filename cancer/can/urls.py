from django.contrib import admin
from django.urls import path
from can.views import *
from rest_framework.routers import DefaultRouter
from can.views import Productviewset
urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Logindata.as_view(), name='login'),
]
router = DefaultRouter()
router.register(r'products', Productviewset,basename='products')



urlpatterns+=router.urls