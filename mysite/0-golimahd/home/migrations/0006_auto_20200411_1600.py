# Generated by Django 3.0.5 on 2020-04-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200411_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headertitle',
            name='title',
            field=models.CharField(max_length=70),
        ),
    ]
