from django import forms
from django.forms import Textarea, DateTimeField
from .models import Post
#from django.forms import MultiWidget
from django.contrib.admin import widgets                                       
from django.utils.translation import gettext_lazy as _
#from django.forms import extras



class PostForm(forms.ModelForm):
    published_date = forms.DateField(widget=forms.SelectDateWidget())
    #created_date = forms.DateField(widget=forms.SelectDateWidget())    #not by this day
    #published_date = forms.DateField(widget=widgets.AdminTimeWidget)
    #published_date = forms.DateField(widget=forms.SelectMultiple())        #for select in items
    #published_date = forms.DateField(widget=forms.SplitDateTimeField())    #for hide
    #published_date = forms.DateField(widget=extras.SelectDateWidget)

    #this is for make selecteble field for date and time
    class Meta:
        model = Post
        #fields = ('author', 'title', 'text', 'draft', 'image_title', 'published_date')
        fields = "__all__"
        
        #begin = DateTimeField(widget=MinimalSplitDateTimeMultiWidget())

