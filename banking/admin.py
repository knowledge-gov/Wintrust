from .models import Security, Beneficiary, Transaction
from django.contrib import admin

# Register your models here.
class SecurityAdmin(admin.ModelAdmin):
    list_display = ('id','otp')
# Register your models here.
admin.site.register(Security, SecurityAdmin)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('id','type','acct_no','routine_no','name')
admin.site.register(Beneficiary, BeneficiaryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','transcation_type','amount','prev_bal','bal')
admin.site.register(Transaction, TransactionAdmin)