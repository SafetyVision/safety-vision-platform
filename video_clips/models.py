from django.db import models

class VideoClip(models.Model):
  file = models.FileField()

  def __str__(self):
    return self.file.url
