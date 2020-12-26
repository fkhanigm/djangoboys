from django.urls import path
from . import views as blog_views
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', blog_views.PostList.as_view(), name='post_list'),
    path('category/<int:pk>', blog_views.CategoryPostList.as_view(), name='category_post_list'),
    path('autor/<int:pk>', blog_views.AuthorPostList.as_view(), name='author_post_list'),
    path('post/<int:pk>/', blog_views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', blog_views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit', blog_views.PostEdit.as_view(), name='post_edit'),
    path('signup/', account_views.SignUp.as_view(), name='signup'),
    path('login/', account_views.LogIn.as_view(), name='login'),
    path('logout/', account_views.LogOut.as_view(), name='logout'),


#    path('page/<int:pageno>', views.PostList.as_view(), name='PostList'),  #for paginator
#    path(r'^$', PostList.as_view(), name='file-exam-view'), 'page/<int:pageno>/', views.index, name='index'    #for pageinator
#    path('articles/2003/',views.special_case_2003),
#    path('articles/<int:year>/',views.year_archive),
#    path('articles/<int:year>/<int:month>/,views.month_archive);
#    path('articles/<int:year>/<int:month>/<slug:slug>/',views.articles_detail),
]
