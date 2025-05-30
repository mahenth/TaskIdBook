from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Add other fields if needed for the base user, e.g., phone_number
    # For username, you can keep the default or make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 'username' will still be required during creation

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"