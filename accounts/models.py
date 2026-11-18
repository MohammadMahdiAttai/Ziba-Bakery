from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True, help_text='Street address for delivery')
    suburb = models.CharField(max_length=100, blank=True, help_text='e.g. Carlton, Fitzroy, St Kilda')
    postcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
