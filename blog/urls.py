from django.urls import path
from . import views as blog_views
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', blog_views.PostList.as_view(), name='post_list'),
    #path(r'^$', PostList.as_view(), name='file-exam-view'), 'page/<int:pageno>/', views.index, name='index'    #for pageinator
    #path('page/<int:pageno>', views.PostList.as_view(), name='PostList'),  #for paginator
    path('post/<int:pk>/', blog_views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', blog_views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit', blog_views.PostEdit.as_view(), name='post_edit'),
    path('signup/', account_views.SignUp.as_view(), name='signup'),
    path('login/', account_views.LogIn.as_view(), name='login'),
    path('logout/', account_views.LogOut.as_view(), name='logout'),

]
