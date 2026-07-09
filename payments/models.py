from django.db import models
from members.models import Member

class Payment(models.Model):
    STATUS_CHOICES = [
        ('paid',    'Paid'),
        ('pending', 'Pending'),
    ]
    METHOD_CHOICES = [
        ('cash',      'Cash'),
        ('easypaisa', 'EasyPaisa'),
        ('jazzcash',  'JazzCash'),
        ('bank',      'Bank Transfer'),
    ]
    member       = models.ForeignKey(
                       Member,
                       on_delete=models.CASCADE)
    amount       = models.DecimalField(
                       max_digits=8,
                       decimal_places=2)
    payment_date = models.DateField(
                       null=True,
                       blank=True)
    due_date     = models.DateField()
    method       = models.CharField(
                       max_length=15,
                       choices=METHOD_CHOICES,
                       blank=True)
    status       = models.CharField(
                       max_length=10,
                       choices=STATUS_CHOICES,
                       default='pending')

    def __str__(self):
        return f"{self.member} - PKR {self.amount} - {self.status}"