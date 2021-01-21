
from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext
from .models import HomeDetail, Images, Gallery
from .forms import HomeDetailForm, ImageForm, GalleryForm
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,DetailView, FormView
from django.template.loader import get_template
from django.template import Context
from django.forms import modelformset_factory


class Index(ListView):
    template_name = "index.html"
    model = HomeDetail
    context_object_name = 'homedetail'
    
def gallery_show(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            for field in request.FILES.keys():
                for formfile in request.FILES.getlist(field):
                    img = Images(image=formfile)
                    img.save()

    else:
        form = ImageForm()
    return render(request, 'galleryForm.html',{'form':form})

#@login_required
#def gallery_show(request):
#    ImageFormSet = modelformset_factory(Images,
#                                        form=ImageForm, extra=3)
#    if request.method == 'POST':
#        galleryForm = GalleryForm(request.POST)
#        formset = ImageFormSet(request.POST, request.FILES,
#                               queryset=Images.objects.none())
#        if galleryForm.is_valid() and formset.is_valid():
#            gallery_form = galleryForm.save(commit=False)
#            gallery_form.user = request.user
#            gallery_form.save()
#            for form in formset.cleaned_data:
#                image = form['image']
#                photo = Images(post=gallery_form, image=image)
#                photo.save()
#            messages.success(request,
#                             "Posted!")
#            return HttpResponseRedirect("/")
#        else:
#            print (galleryForm.errors, formset.errors)
#    else:
#        galleryForm = GalleryForm()
#        formset = ImageFormSet(queryset=Images.objects.none())
#    return render(request, 'galleryForm',
#                  {'galleryForm': galleryForm, 'formset': formset},
#                  context_instance=RequestContext(request))


    #def get(self, request, *args, **kwargs):
    #    context = self.get_context_data(**kwargs)
    #    return self.render_to_response(context)


    #model = HomeDetail
    #context_object_name = 'homedetail'
    #template_name = "index.html"
    #queryset = HomeDetail.objects.all()
#class Index(FormView):
#    template_name = "index.html"
#    form_class = HomeDetailForm
#    success_url = 'home'
#from django.views.generic import ListView,DetailView, FormView
#from django.views.generic.edit import CreateView
#from django.urls import reverse_lazy 
#from django.core.paginator import Paginator
#from django.shortcuts import render, HttpResponse
#from django.shortcuts import render, get_object_or_404, redirect
#from django.utils import timezone
#def index(request):
#    homedetail = HomeDetail.objects.all()
#    
#    return render (request, 'index.html',{'homedetail':homedetail})

