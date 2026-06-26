from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('vehicleDisplay/', vehicleDisplay, name='vehicleDisplay'),
    path('carsingle/<int:id>/', carsingle, name='carsingle'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('book/<int:id>', book_vehicle, name='book_vehicle'),
]
