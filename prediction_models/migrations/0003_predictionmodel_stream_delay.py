# Generated by Django 3.2.9 on 2022-03-31 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_models', '0002_predictionmodel_training_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionmodel',
            name='stream_delay',
            field=models.IntegerField(default=0),
        ),
    ]
