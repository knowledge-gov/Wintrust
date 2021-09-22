from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Security(models.Model):
    otp = models.CharField(max_length=255)


class Beneficiary(models.Model):
    type = models.CharField(max_length=255)
    acct_no = models.CharField(max_length=255)
    routine_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)


class Transaction(models.Model):
    transcation_type = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    prev_bal =  models.CharField(max_length=255)
    bal = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    trans_date = CharField(max_length=255)


class CardDetails(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    apt_unit = models.CharField(max_length=255)
    cvv = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)



