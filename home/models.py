from django.db import models

# Create your models here.
class Register(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    account_No = models.CharField(max_length=255, default='673872394219')
    routine = models.CharField(max_length=255, default='071925444')
    balance = models.FloatField(max_length=255)
    userid = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    

