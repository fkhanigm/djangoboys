from django.urls import path, re_path
from .views import home, post_single, categories_archive, category_single, login_view, logout_view, register_view

urlpatterns = [
    path('posts/', home, name='posts_archive'),
    path('posts/<slug:pk>/', post_single, name='post_single'),
    path('categories/', categories_archive, name='categories_archive'),
    path('categories/<slug:pk>/', category_single, name='category_single'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

]
