# Generated by Django 3.1.4 on 2020-12-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201225_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.JSONField(blank=True, db_index=True, null=True),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
