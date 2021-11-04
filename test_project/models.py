from django.db import models

class Test(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description