from django.contrib import admin
from .models import Register


class RegisterAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','phone')
# Register your models here.
admin.site.register(Register, RegisterAdmin)

