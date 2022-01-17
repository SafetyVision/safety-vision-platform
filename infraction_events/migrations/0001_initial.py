# Generated by Django 3.2.9 on 2022-01-17 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('video_clips', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfractionEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infraction_date_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('infraction_video', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_clips.videoclip')),
            ],
        ),
    ]
