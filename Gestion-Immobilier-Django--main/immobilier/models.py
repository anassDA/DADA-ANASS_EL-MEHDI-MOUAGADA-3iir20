from django.db import models

class Immobilier(models.Model):
    titre = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
   
    image = models.CharField(max_length=255, blank=True, null=True)  
    
    def __str__(self):
        return self.titre