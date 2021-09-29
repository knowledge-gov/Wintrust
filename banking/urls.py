from banking.models import Beneficiary
from django.urls import path
from . import views
from home.views import index


urlpatterns=[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardHome/', views.dash, name='dash'),
    path('transfer/',views.transfer, name = 'transfer'),
    path('processtransfer/', views.beneficiary, name= 'add_beneficiary'),
    path('linkcard/', views.linkcard, name= 'linkcard'),
    path('billpay/', views.billpay, name= 'bill'),
    path('auth/',views.auth,name='auth'),
    path('logout/',index,name='logout'),
    path(r'',views.index2,name = 'banking')
]