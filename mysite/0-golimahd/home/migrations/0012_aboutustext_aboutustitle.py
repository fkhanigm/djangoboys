# Generated by Django 3.0.5 on 2020-04-13 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aboutustext', models.CharField(max_length=1500, verbose_name='aboutustext')),
            ],
        ),
        migrations.CreateModel(
            name='AboutUsTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aboutustitle', models.CharField(max_length=70, verbose_name='aboutustitle')),
            ],
        ),
    ]
