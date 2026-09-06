from django.db import models
from accounts.models import User

class Trainer(models.Model):
    SPEC_CHOICES = [
        ('weight',   'Weight Training'),
        ('cardio',   'Cardio & Fitness'),
        ('yoga',     'Yoga & Flexibility'),
    ]
    user           = models.OneToOneField(
                         User,
                         on_delete=models.CASCADE)
    specialization = models.CharField(
                         max_length=15,
                         choices=SPEC_CHOICES,
                         default='weight')
    salary         = models.DecimalField(
                         max_digits=8,
                         decimal_places=2,
                         default=0)
    join_date      = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()