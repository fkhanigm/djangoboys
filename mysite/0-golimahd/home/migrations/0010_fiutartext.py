# Generated by Django 3.0.5 on 2020-04-13 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200413_0746'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiutarText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text1', models.CharField(max_length=1000, verbose_name='text1')),
            ],
        ),
    ]
