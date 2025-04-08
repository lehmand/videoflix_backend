from django.db import models

# Create your models here.

class Video(models.Model):
  uploaded_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=150)
  description = models.TextField(max_length=1000, blank=True)
  file = models.FileField(upload_to='uploads/videos')
  thumbnail = models.FileField(upload_to='uploads/thumbnails')
  genre = models.CharField(max_length=150, blank=True)

  def __str__(self):
    return self.title