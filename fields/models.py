from django.db import models
from users.models import User
# Create your models here.

class Field(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    # location = models.PointField()  # (longitude, latitude)
    images = models.JSONField(default=list)  # Rasmlar

    def __str__(self):
        return self.name