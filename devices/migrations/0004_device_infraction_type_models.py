# Generated by Django 3.2.9 on 2022-02-24 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_models', '0001_initial'),
        ('infraction_types', '0003_auto_20220224_0353'),
        ('devices', '0003_auto_20220219_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='infraction_type_models',
            field=models.ManyToManyField(through='prediction_models.PredictionModel', to='infraction_types.InfractionType'),
        ),
    ]