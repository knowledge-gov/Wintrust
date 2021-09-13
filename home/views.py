from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

def index(request):
    return render(request,'home.html')


def reg(request):
    return render(request,'reg.html')


def register(request):
    acct = random.randint(100000000000,999999999999)

    first_name  = request.POST['fname']
    last_name =  request.POST['lname']
    email = request.POST['email']
    phone = request.POST['area_code'] + request.POST['phone']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zip = request.POST['zip']
    acount_no = request.POST['accountNo']
    routine = request.POST['routine']
    balance = request.POST['balance']
    userId = request.POST['userId']
    password = request.POST['password']
    password2 = request.POST['password2']

    return render(request, 'index.html',{'result': acct})