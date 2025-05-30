from django.db import models
from django.db import models
from users.models import User # Import your custom user model
from hotels.models import Hotel

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()
    no_of_persons = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking by {self.user.email} at {self.hotel.name}"