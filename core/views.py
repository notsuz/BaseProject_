from django.shortcuts import render
from .models import Vehicles

# Create your views here.
def index(request):
    vehicle=Vehicles.objects.all()
    
    
    context={
        'vehicle': vehicle
    }
    return render(request, "core/index.html", context)

def carsingle(request):
    return render(request, 'core/carsingle.html')
    