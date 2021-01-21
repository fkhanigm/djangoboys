from django import forms

from .models import HomeDetail, Gallery, Images

class HomeDetailForm(forms.ModelForm):

    class Meta:
        model = HomeDetail
        fields = ('main_title1', 'main_title2', 'main_text1', 'about_us_image', 'about_us_text')


class GalleryForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=1000)

    class Meta:
        model = Gallery
        fields = ('title', 'body', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField()    
    class Meta:
        model = Images
        fields = ('image', )



