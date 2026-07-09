from django.db import models
from trainers.models import Trainer

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
        ('all',          'All Levels'),
    ]
    title       = models.CharField(max_length=200)
    description = models.TextField()
    trainer     = models.ForeignKey(
                      Trainer,
                      on_delete=models.SET_NULL,
                      null=True)
    level       = models.CharField(
                      max_length=15,
                      choices=LEVEL_CHOICES,
                      default='beginner')
    duration    = models.CharField(max_length=50)
    image       = models.ImageField(
                      upload_to='courses/',
                      blank=True,
                      null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    TYPE_CHOICES = [
        ('Pdf',     'Pdf'),
        ('routine', 'Routine'),
    ]
    course       = models.ForeignKey(
                       Course,
                       on_delete=models.CASCADE)
    title        = models.CharField(max_length=200)
    content_type = models.CharField(
                       max_length=10,
                       choices=TYPE_CHOICES)
    file         = models.FileField(
                       upload_to='course_files/')
    uploaded_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title