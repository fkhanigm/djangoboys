# Generated by Django 3.1.4 on 2020-12-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_image_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_title',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
