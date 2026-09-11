from django.db import models
from accounts.models import User

class Member(models.Model):
    PLAN_CHOICES = [
        ('basic',    'Basic  PKR 2000'),
        ('standard', 'Standard  PKR 3500'),
        ('premium',  'Premium  PKR 5000'),
    ]
    user             = models.OneToOneField(
                           User,
                           on_delete=models.CASCADE)
    age              = models.IntegerField(default=0)
    weight           = models.DecimalField(
                           max_digits=5,
                           decimal_places=2,
                           default=0)
    membership_plan  = models.CharField(
                           max_length=10,
                           choices=PLAN_CHOICES,
                           default='basic')
    assigned_trainer = models.ForeignKey(
                           'trainers.Trainer',
                           on_delete=models.SET_NULL,
                           null=True,
                           blank=True)
    join_date        = models.DateField(auto_now_add=True)
    is_active        = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()