from django.contrib import admin
from .models import Vehicles, Category

admin.site.register(Category)
# Register your models here.
@admin.register(Vehicles)
class VechileAdmin(admin.ModelAdmin):
    list_display=['title', 'vehicle_type', 'price_per_day', 'is_approved']