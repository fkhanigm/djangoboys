#from django.contrib.auth.models import User
#from django.conf import settings
#User = settings.AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re
from django.contrib.auth import get_user_model
User = get_user_model()


def validate_password(password):
    if len(password) < 8:
        raise ValidationError(_('password is too short!'), code='invalid')
    if len(password) > 150:
        raise ValidationError(_('password is too long!'), code='invalid')


def validate_username(username):
    try:
        User.objects.get(username=username)
        raise ValidationError(_('this username already exist!'), code='invalid')
    except User.DoesNotExist:
        pass
