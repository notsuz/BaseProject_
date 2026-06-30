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
    


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # 1. Adds clear columns so you can see status, dates, etc.
    list_display = ('id', '__str__', 'status', 'start_date', 'end_date')
    
    # 2. OPTION A: Allows you to change the status dropdown right on the list grid!
    list_editable = ('status',)
    
    # 3. OPTION B: Adds custom options into the 'Action' dropdown menu from your screenshot
    actions = ['approve_bookings', 'cancel_bookings']

    @admin.action(description='Mark selected bookings as Approved')
    def approve_bookings(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Mark selected bookings as Cancelled')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')