"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account.api import UserViewSet
from rest_framework import routers
	
router = routers.DefaultRouter()
	
router.register(r'users', UserViewSet)
	
urlpatterns = [
	path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('api-auth/', include('rest_framework.urls'))

    #path('articles/2003/',views.special_case_2003),
    #path('articles/<int:year>/',views.year_archive),
    #path('articles/<int:year>/<int:month>/,views.month_archive);
    #path('articles/<int:year>/<int:month>/<slug:slug>/',views.articles_detail),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

