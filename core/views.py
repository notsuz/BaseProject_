from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicles,Review
from .forms import ReviewForm
from django.db.models import Avg

# Create your views here.
def index(request):
    vehicle=Vehicles.objects.all()
    
    
    context={
        'vehicle': vehicle
    }
    return render(request, "core/index.html", context)

def carsingle(request, id):
    uniVehicles = get_object_or_404(Vehicles, id=id)
    
    reviews = Review.objects.filter(vehicle=uniVehicles)
    review_count = reviews.count()
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.vehicle = uniVehicles 
            review.save()
            return redirect('carsingle', id=uniVehicles.id)    
    else:
        form = ReviewForm()
    
    context = {
        'uniVehicles': uniVehicles,
       
        'vehicle': uniVehicles, 
        'form': form,
        'reviews': reviews,
        'review_count': review_count,
        'range': range(1, 6),  # Makes star loops work natively
        'avg_rating': round(avg_rating) if avg_rating else 0,
    }
    
    return render(request, 'core/carsingle.html', context)

def vehicleDisplay(request):
    vehicle=Vehicles.objects.all()
    
    context={
        'vehicle': vehicle
    }
    return render(request, 'core/vehicleDisplay.html', context)
    