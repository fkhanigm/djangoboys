from django.urls import path, include
from . import views as blog_views
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static
from . import api
from mysite.urls import router

	
router.register(r'posts', api.PostViewSet)
router.register(r'comments', api.CommentViewSet)
router.register(r'categoryes', api.CategoryViewSet)


urlpatterns = [
    path('', blog_views.PostList.as_view(), name='post_list'),
    path('category/<int:pk>', blog_views.CategoryPostList.as_view(), name='category_post_list'),
    path('autor/<int:pk>', blog_views.AuthorPostList.as_view(), name='author_post_list'),
    path('post/<int:pk>/', blog_views.PostDetail.as_view(), name='post_detail'),
    #path('like_comment/<slug:post_pk>/', blog_views.like_comment, name='like_comment'),
    #path('post/<slug:slug>/', blog_views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', blog_views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit', blog_views.PostEdit.as_view(), name='post_edit'),
    path('signup/', account_views.SignUp.as_view(), name='signup'),
    path('accounts/login/', account_views.LogIn.as_view(), name='login'),
    path('logout/', account_views.LogOut.as_view(), name='logout'),
    path('like_comment/', blog_views.like_comment, name='like_comment'),
    path('comment/', blog_views.create_comment, name='add_comment'),
    #path('json/comments/',api.comment_list, name='comment_list_api'),
    #path('json/comments/<int:pk>',api.comment_detail, name='comment_detail_api'),
    #path('json/posts/',api.post_list, name='post_list_api'),
    #path('json/posts/<int:pk>',api.post_detail, name='post_detail_api'),
    #path('json/posts/',api.PostList.as_view(), name='post_list_api'),
    #path('json/posts/<int:pk>',api.PostDetail.as_view(), name='post_detail_api'),
    #path('json/posts/',api.PostListMixin.as_view(), name='post_list_api'),
    #path('json/posts/<int:pk>',api.PostDetailMixin.as_view(), name='post_detail_api'),
    #path('json/posts/',api.PostListGeneric.as_view(), name='post_list_api'),
    #path('json/posts/<int:pk>',api.PostdetailGeneric.as_view(), name='post_detail_api'),
    path('json/posts/',api.PostViewSet.as_view({
        'get':'list', 
        'post':'create'}), name='post_list_api'),
        #attention:did not show actions in this type of url,need router
    path('json/posts/<int:pk>/',api.PostViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    }), name='post_detail_api'),
        #attention:did not show actions in this type of url,need router
    path('json/comments/',api.CommentViewSet.as_view({
        'get':'list', 
        'post':'create'}), name='comment_list_api'),
        #attention:did not show actions in this type of url,need router
    path('json/comments/<int:pk>/',api.CommentViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    }), name='comment_detail_api'),
        #attention:did not show actions in this type of url,need router
    path('json/categories/',api.CategoryViewSet.as_view({
        'get':'list', 
        'post':'create'}), name='comment_list_api'),
        #attention:did not show actions in this type of url,need router
    path('json/categories/<int:pk>/',api.CategoryViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    }), name='comment_detail_api'),
        #attention:did not show actions in this type of url,need router



#    path('page/<int:pageno>', views.PostList.as_view(), name='PostList'),  #for paginator
#    path(r'^$', PostList.as_view(), name='file-exam-view'), 'page/<int:pageno>/', views.index, name='index'    #for pageinator
#    path('articles/2003/',views.special_case_2003),
#    path('articles/<int:year>/',views.year_archive),
#    path('articles/<int:year>/<int:month>/,views.month_archive);
#    path('articles/<int:year>/<int:month>/<slug:slug>/',views.articles_detail),
]
#urlpatterns = format_suffix_patterns(urlpatterns)