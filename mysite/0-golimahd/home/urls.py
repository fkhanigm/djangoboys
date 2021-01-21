from django.urls import path
from . import views

urlpatterns = [
     path('', views.Index.as_view(), name='home'),
     path('galleryForm/', views.gallery_show, name='galleryForm'),
    
]
