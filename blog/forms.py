from django import forms
from django.forms import Textarea, DateTimeField
from .models import Post, Comment, CommentLike
#from django.forms import MultiWidget
from django.contrib.admin import widgets                                       
from django.utils.translation import gettext_lazy as _
#from django.forms import extras
#from django.contrib.auth import get_user_model
#User = get_user_model


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
        fields = ('title', 'slug', 'text', 'image_title', 'published_date', 'draft', 'category')
        #fields = "__all__"
        #begin = DateTimeField(widget=MinimalSplitDateTimeMultiWidget())
    #def clean_slug(self): #???
    #    slug = self.cleaned_data.get('slug')
    #    slug_validator(slug)
    #    return slug

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )#fields to show in html
        labels = {'text':_('enter your comment'), }#label on top of the box
        widgets = {'text':forms.Textarea}#???

class CommentLikeForm(forms.ModelForm):
    condition = forms.CharField()
    comment = forms.IntegerField()

    def clean_condition(self):
        condition = self.clean_data['condition']
        return condition =='true'
        