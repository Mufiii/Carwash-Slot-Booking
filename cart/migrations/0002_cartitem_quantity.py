# Generated by Django 4.2.2 on 2023-07-25 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]