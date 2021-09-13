import banking
from django.contrib import admin
from django.urls import path
from . import views
from banking.views import index2

urlpatterns=[
    path(r'',views.index, name='home'),
    path('banking/',index2, name= 'bank'),
    path('reg/',views.reg,name='reg'),
    path('register/',views.register,name='register'),
]