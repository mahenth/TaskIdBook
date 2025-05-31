from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)
    # Add other hotel details like ratings, amenities, etc.

    def __str__(self):
        return self.name