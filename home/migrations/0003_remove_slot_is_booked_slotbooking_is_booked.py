# Generated by Django 4.2.2 on 2023-08-01 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='is_booked',
        ),
        migrations.AddField(
            model_name='slotbooking',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
