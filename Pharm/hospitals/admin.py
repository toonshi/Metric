from django.contrib import admin
from .models import Service, Insurance

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_price', 'institution')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('insurance_name', 'institution')
