from django.db import models
from django.conf import settings
from django.utils import timezone  # Django's standard for handling local/server time safely
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    
    
class Vehicles(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    vehicle_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_currently_booked(self):
        # Using timezone.now().date() keeps your time evaluations consistent with the server clock
        today = timezone.now().date() 
        
        # 🛠️ FIX: Added '__in' so Django scans the contents of your list entries
        return self.bookings.filter(
            status__in=['approved', 'pending'],
            start_date__lte=today,
            end_date__gte=today
        ).exists()
    
    
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.vehicle.title

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    feedback = models.TextField()
    created_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.vehicle.title
    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_bookings')
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='bookings')
    
    full_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    verified_document = models.FileField(upload_to='booking_documents/')
    
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.vehicle.title} ({self.start_date} to {self.end_date})"

    @property
    def remaining_days(self):
        today = timezone.now().date()
        
        if today < self.start_date:
            return (self.end_date - self.start_date).days
        elif today > self.end_date:
            return 0
        else:
            return (self.end_date - today).days