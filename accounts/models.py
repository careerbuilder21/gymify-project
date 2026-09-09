from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('trainer', 'Trainer'),
        ('member',  'Member'),
    ]
    role             = models.CharField(
                           max_length=10,
                           choices=ROLE_CHOICES,
                           default='member')
    phone            = models.CharField(
                           max_length=15,
                           blank=True)
    security_answer  = models.CharField(
                           max_length=100,
                           blank=True)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"