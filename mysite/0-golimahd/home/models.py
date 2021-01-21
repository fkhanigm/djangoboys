from django.db import models
#from __future__ import unicode_literals
#from uuid import uuid4
#import os
#import re
#from django.contrib.auth.models import User


class HomeDetail(models.Model):
    main_title1 = models.CharField('main_title1', max_length=70, null=True)
    main_title2 = models.CharField('main_title2', max_length=70, null=True)
    main_text1 = models.CharField('main_text1', max_length=1000, null=True)
    about_us_image = models.ImageField(upload_to='', null=True, blank=True)
    about_us_text = models.CharField('about_us_text', max_length=1500, null=True)
    

    def __str__(self):
        return self.main_title1.name


class Gallery(models.Model):
    title = models.CharField(max_length=128, null=True)
    body = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.title.name

 
class Images(models.Model):
    image = models.ImageField(upload_to='',null=True, blank=True)
    def __str__(self):
        return self.image.name