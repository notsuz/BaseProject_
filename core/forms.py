from django import forms
from .models import Review
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['rating','feedback']
        

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'license_number', 'verified_document', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Legal Full Name'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Identification Number'}),
            'verified_document': forms.FileInput(attrs={'class': 'form-control'}),
        }