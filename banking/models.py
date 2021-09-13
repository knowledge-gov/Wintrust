from django.db import models

# Create your models here.
class Security(models.Model):
    otp = models.CharField(max_length=255)


class Beneficiary(models.Model):
    type = models.CharField(max_length=255)
    acct_no = models.CharField(max_length=255)
    routine_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Transaction(models.Model):
    transcation_type = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    prev_bal =  models.CharField(max_length=255)
    bal = models.CharField(max_length=255)
    name = models.CharField(max_length=255)



