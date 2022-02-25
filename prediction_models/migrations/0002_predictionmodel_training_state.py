# Generated by Django 3.2.9 on 2022-02-25 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionmodel',
            name='training_state',
            field=models.CharField(choices=[('0', 'Initialized'), ('1', 'First committing infraction'), ('2', 'Done committing first infraction'), ('3', 'First not committing infraction'), ('4', 'First done not commimtting infraction'), ('5', 'Second committing infraction'), ('6', 'Done committing second infraction'), ('7', 'Second not committing infraction'), ('8', 'Done not commimtting second infraction'), ('9', 'Trained')], default='0', max_length=1),
        ),
    ]
