from django import forms
from .models import Immobilier

class ImmobilierForm(forms.ModelForm):
    class Meta:
        model = Immobilier
        fields = ['titre', 'adresse', 'prix', 'description', 'image'] 
