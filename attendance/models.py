from django.db import models
from members.models import Member
from trainers.models import Trainer

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
    ]
    member       = models.ForeignKey(
                       Member,
                       on_delete=models.CASCADE)
    marked_by    = models.ForeignKey(
                       Trainer,
                       on_delete=models.SET_NULL,
                       null=True)
    date         = models.DateField()
    checkin_time = models.TimeField(
                       null=True,
                       blank=True)
    status       = models.CharField(
                       max_length=10,
                       choices=STATUS_CHOICES,
                       default='absent')

    class Meta:
        unique_together = ['member', 'date']

    def __str__(self):
        return f"{self.member} - {self.date} - {self.status}"