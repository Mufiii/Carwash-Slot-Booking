# Generated by Django 4.2.2 on 2023-08-16 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
