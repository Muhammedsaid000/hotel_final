# Generated by Django 5.1.3 on 2024-12-07 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_room_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_hotel', to='hotels.hotel'),
        ),
    ]
