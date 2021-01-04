from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.utils.translation import gettext_lazy as _




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #had defauld valiation
    class Meta: #کمک کننده تعریف ویژگیپ ها کلاس نه آبجکت ها
        model = User
        #email_addres Display_name avatar is_staff is_activ
        fields = ('email', 'full_name', 'avatar')
        labels = {
            'email':_('ایمیل'), 
            'password':_('رمز عبور'), 
            'password2':_('تکرار رمز عبور'),
            'fullname':_('نام کامل')
            }
        widget = {
            'email':forms.EmailField(),#attrs={'class':'form-control'}
            'password':forms.PasswordInput(),#attrs={'class':'form-control'}
            'password2':forms.PasswordInput(),#attrs={'class':'form-control'}
            'fullname':forms.TextInput()#attrs={'class':'form-control'}
        }
        help_text = {'email':_('a valid email for reser your password'), }

#make our oun singin form
#from django.contrib.auth.forms import AuthenticationForm
#class SignInForm(AuthenticationForm):
#   def clean(self):
#       cleaned_data = super().clean()
#       ....
#       ....
#       return cleaned_data