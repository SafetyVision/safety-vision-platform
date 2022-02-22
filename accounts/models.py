from django.db import models

class Account(models.Model):
    account_name = models.CharField(max_length=75)
    owner = models.ForeignKey(
        'users.ExtendedUser',
        on_delete=models.CASCADE,
        related_name='owned_account',
        default=None,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_name
