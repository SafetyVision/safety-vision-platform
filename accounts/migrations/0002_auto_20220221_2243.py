# Generated by Django 3.2.9 on 2022-02-21 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='login_identifier',
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_account', to=settings.AUTH_USER_MODEL),
        ),
    ]
