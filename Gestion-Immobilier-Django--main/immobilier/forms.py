from django import forms
from .models import Immobilier
from django.core.validators import MinValueValidator

class ImmobilierForm(forms.ModelForm):
    prix = forms.DecimalField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix en €'
        })
    )
    
    class Meta:
        model = Immobilier
        fields = ['titre', 'adresse', 'prix', 'description', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du bien'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description détaillée...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'titre': 'Titre',
            'adresse': 'Adresse',
            'prix': 'Prix (MAD)',
            'description': 'Description',
            'image': 'Photo du bien'
        }

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0")
        return prix

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:  # 5MB max
                raise forms.ValidationError("L'image ne doit pas dépasser 5MB")
            return image
        return image