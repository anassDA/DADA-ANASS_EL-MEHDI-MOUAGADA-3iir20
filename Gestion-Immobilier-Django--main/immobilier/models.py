from django.db import models
from django.contrib.auth.models import User

class Immobilier(models.Model):
    titre = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    disponible = models.BooleanField(default=True)
    reserved_by = models.ManyToManyField(User, through='Reservation', blank=True, related_name='reservations')

    def __str__(self):
        return self.titre

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    immobilier = models.ForeignKey(Immobilier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'immobilier')

    def __str__(self):
        return f"{self.user.username} - {self.immobilier.titre}"

class Notification(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)  
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New reservation: {self.reservation.immobilier.titre}"
        