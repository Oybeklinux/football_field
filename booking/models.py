from django.db import models
from users.models import User
from fields.models import Field
# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
   

    def __str__(self):
        return f"{self.user.username} - {self.field.name}"