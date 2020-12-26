from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #had defauld valiation
    class Meta: #کمک کننده تعریف ویژگیپ ها کلاس نه آبجکت ها
        model = User
        #email_addres Display_name avatar is_staff is_activ
        fields = ('email', 'full_name','avatar')
