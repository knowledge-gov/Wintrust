from banking.models import Beneficiary
from django.urls import path
from . import views


urlpatterns=[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardHome/', views.dash, name='dash'),
    path('transfer/',views.transfer, name = 'transfer'),
    path('processtransfer/', views.beneficiary, name= 'add_beneficiary'),
    path('linkcard/', views.linkcard, name= 'linkcard'),
    path('auth/',views.auth,name='auth'),
    path(r'',views.index2,name = 'banking')
]