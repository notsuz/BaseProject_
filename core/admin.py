from django.contrib import admin
from .models import *

admin.site.register(Category)



class VehicleImageAdmin(admin.TabularInline):
    model=VehicleImage
    extra=1
    
@admin.register(Vehicles)
class VehicleAdmin(admin.ModelAdmin):
    list_display=['title', 'vehicle_type', 'price_per_day', 'is_approved']
    inlines=[VehicleImageAdmin]