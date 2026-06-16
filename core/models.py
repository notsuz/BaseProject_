from django.db import models
from datetime import datetime
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title
    
    
class Vehicles(models.Model):
    title=models.CharField(max_length=200)
    description = models.TextField()
    vehicle_type = models.ForeignKey(Category, on_delete=models.CASCADE) # Car, Bike, Scooter
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')
    latitude = models.FloatField(blank=True, null=True) # For map integration
    longitude = models.FloatField(blank=True, null=True)
    is_approved = models.BooleanField(default=False) # Admin verification flag
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.vehicle.title
    

    
