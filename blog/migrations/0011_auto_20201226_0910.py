# Generated by Django 3.1.4 on 2020-12-26 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20201225_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, verbose_name='slug'),
        ),
    ]