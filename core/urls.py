from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('vehicleDisplay/', vehicleDisplay, name='vehicleDisplay'),
    path('carsingle/<int:id>/', carsingle, name='carsingle'),
]
