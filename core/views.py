from django.shortcuts import render, get_object_or_404
from .models import Vehicles

# Create your views here.
def index(request):
    vehicle=Vehicles.objects.all()
    
    
    context={
        'vehicle': vehicle
    }
    return render(request, "core/index.html", context)

def carsingle(request, id):
    uniVehicles=get_object_or_404(Vehicles,id=id)
    
    context={
        'uniVehicles': uniVehicles
    }
    
    return render(request, 'core/carsingle.html', context)

def vehicleDisplay(request):
    vehicle=Vehicles.objects.all()
    
    context={
        'vehicle': vehicle
    }
    return render(request, 'core/vehicleDisplay.html', context)
    