# Generated by Django 2.2.13 on 2020-08-04 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NEMO', '0021_version_3_1_0'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='count_service_personnel_in_occupancy',
            field=models.BooleanField(default=True, help_text='Indicates that service personnel will count towards maximum capacity.'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_service_personnel',
            field=models.BooleanField(default=False, help_text='Designates this user as service personnel. Service personnel can operate qualified tools without a reservation even when they are shutdown or during an outage and can access authorized areas without a reservation.', verbose_name='service personnel'),
        ),
        migrations.AddField(
            model_name='consumable',
            name='reminder_threshold_reached',
            field=models.BooleanField(default=False),
        ),
    ]
