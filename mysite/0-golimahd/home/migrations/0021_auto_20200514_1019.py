# Generated by Django 3.0.6 on 2020-05-14 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20200514_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='gallery',
            new_name='post',
        ),
    ]
