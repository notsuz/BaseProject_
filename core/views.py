from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import ReviewForm
from django.db.models.functions import Coalesce
from django.db.models import Avg, Value
from .forms import BookingForm

# Create your views here.
def index(request):
    vehicle=Vehicles.objects.all()
    top_product = Vehicles.objects.annotate(
        top_rating=Coalesce(Avg('reviews__rating'), Value(0.0))
    ).order_by('-top_rating')[:3]
    
    
    context={
        'vehicle': vehicle,
        'top_product': top_product
    }
    return render(request, "core/index.html", context)

def carsingle(request, id):
    uniVehicles = get_object_or_404(Vehicles, id=id)
    reviews = uniVehicles.reviews.all()
    # reviews = Review.objects.filter(vehicle=uniVehicles)
    
    review_count = reviews.count()
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.vehicle = uniVehicles 
            review.save()
            return redirect('carsingle', id=uniVehicles.id)    
        
    related_vehicle=Vehicles.objects.filter(vehicle_type=uniVehicles.vehicle_type).exclude(id=uniVehicles.id)
    
    context = {
        'uniVehicles': uniVehicles, 
        'form': form,
        'reviews': reviews,
        'review_count': review_count,
        'range': range(1, 6),  # Makes star loops work natively
        'avg_rating': round(avg_rating) if avg_rating else 0,
        'related_vehicle':related_vehicle
    }
    
    return render(request, 'core/carsingle.html', context)

def vehicleDisplay(request):
    vehicle=Vehicles.objects.all()
    
    context={
        'vehicle': vehicle
    }
    return render(request, 'core/vehicleDisplay.html', context)


#booking vechile logic
@login_required
def book_vehicle(request, id):
    vehicle = get_object_or_404(Vehicles, id=id)
    
    if request.method == "POST":
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.vehicle = vehicle
            
            #checking for overlaps / same vehicle booking by 2 or more users / {recheck}
            overlapping_bookings = Booking.objects.filter(
                vehicle=vehicle,
                status__in=['approved', 'pending'],
                start_date__lte=booking.end_date,
                end_date__gte=booking.start_date
            )
            
            if overlapping_bookings.exists():
                messages.error(request, "This vehicle is already locked for those exact calendar dates!")
            else:
                duration = booking.end_date - booking.start_date
                rental_days = duration.days
                
                if rental_days <= 0:
                    messages.error(request, "Invalid timeline. End date must follow your start date.")
                else:
                    booking.total_price = rental_days * vehicle.price_per_day
                    booking.save()
                    messages.success(request, "Your booking request has been locked and sent to Admin!")
                    return redirect('user_dashboard')
    else:
        form = BookingForm()
        
    return render(request, 'core/book_vehicle.html', {'vehicle': vehicle, 'form': form})
    
    
@login_required
def user_dashboard(request):
    # Isolates data records down exclusively to the unique authenticated profile key
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'bookings': user_bookings})