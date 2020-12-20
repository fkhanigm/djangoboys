from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200)
    text = models.TextField(_('text'))
    created_date = models.DateTimeField(_('create date'), default=timezone.now)
    published_date = models.DateTimeField(_('publish date'), blank=True, null=True)
    #slug = models.SlugField(_('slug'), db_index=True, unique=True)
    image_title = models.ImageField(_('image'), upload_to='post/images')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title