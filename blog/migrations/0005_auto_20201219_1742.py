# Generated by Django 3.1.4 on 2020-12-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201219_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_title',
            field=models.ImageField(upload_to='images'),
        ),
    ]
