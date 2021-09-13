from banking.models import Beneficiary
from django.urls import path
from . import views


urlpatterns=[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/',views.transfer, name = 'transfer'),
    path('beneficiary/', views.beneficiary, name= 'add_beneficiary'),
    path('auth/',views.auth,name='auth'),
    path(r'',views.index2,name = 'banking')
]