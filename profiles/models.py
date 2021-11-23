from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts import models as accountsModels

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.ForeignKey(accountsModels.Account, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
