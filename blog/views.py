#from django.shortcuts import render, get_object_or_404, redirect
#from django.utils import timezone
from .forms import PostForm, CommentForm, CommentLikeForm
from datetime import datetime
from .models import Post, Category, Comment, CommentLike
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import models
#from account.models import User
from django.contrib.auth import get_user_model
User = get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django import forms
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin
import json
from django.core.exceptions import ObjectDoesNotExist


#for log in required in class based views
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
class PostEdit(UpdateView):#(LoginRequiredMixin, PermissionRequiredMixin, UpdateView)
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'
    #prtmission_required = 'blog.view_post'
    #prtmission_required = ('blog.delete_post', 'blog.view_post')
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(draft=False, published_date__lte=datetime.now())
    #queryset = Post.objects.all()
    ordering = ('-published_date', '-id')
#    template_name = 'blog/post_list.html'
    paginate_by = '3'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
#        context['users_image'] = User.objects.all()
        return context


class CategoryPostList(ListView):
#run this class without template
    model = Post
    template_name = 'blog/category_post_list.html'
    paginate_by = '3'

    def get_context_data(self, **kwargs):#for find category list in header
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context

    def get_queryset(self):#for find post related by our target category
        #for filter post for each category
        return Post.objects.filter(category_id=self.kwargs.get('pk'))


class AuthorPostList(PostList):
    model = Post
    template_name = 'blog/author_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        #context['author'] = User.objects.all() 
        return context

    def get_queryset(self):
        #for filter post for each category
        return Post.objects.filter(author_id=self.kwargs.get('pk'))


class CategoryList(ListView):
    model = Category
    template_name = 'blog/base.html'


#@method_decorator(csrf_exempt, name='dispatch')
class PostDetail(FormMixin, DetailView):
    model = Post
#    permission_required = ('blog.view_post', 'blog.comment_view')#???
    template_name = 'blog/post_detail.html'
    form_class = CommentForm #not effect

    def get_success_url(self): #for redirect to this page
        return reverse('post_detail', kwargs={'pk': self.object.pk})#read from pk in url

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = context["post"]
        context["category_list"] = Category.objects.all()
        context["comments"] = post.comments.all()#show comments for this post
#        #context['form'] = self.get_form()#import form of write comment
#        #context['form'] = CommentForm(initial={'post': self.object})#import form of write comment
        return context

    def post(self, request, *args, **kwargs):#for get comment form
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):#for validation and commit emty field
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        form = form.save(commit=False)
        form.author = self.request.user#commit author field
        form.post = Post.objects.get(pk=self.kwargs.get('pk'))#comit post field
        form.save()#save form
        return super().form_valid(form)


class PostNew(LoginRequiredMixin, CreateView):
    #login_url = 'login'
    #redirect_field_name = 'post_list'
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(
            reverse(
                'post_list', 
                #args=(question.id,)
                )
            )

@csrf_exempt    #for ignor csrf token
def like_comment(request):
    #for use ajax
    '''for time we did not have serializer.so we did not use rest_full. this is just a small rest for handel the like_comment
    when we have just two or three rest did not usual use 3MB library of restFULL we can handel that whit ajax'''
    data = json.loads(request.body)
    #for change the json to dictionery
    user = request.user 
    #get log in user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
        #check we have this comment or not,we should not trust to frontEnd evr. we should check the all requests by our self
    except  Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
        #the comment does not exist
    try:
        comment_like = CommentLike.objects.get(author=user, comment= comment)
        #to check the user is like this comment befor
        comment_like.condition = data['condition']
        comment_like.save()
        #if comment like is exist change the condition
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(
            author=user, 
            comment= comment,
            condition=data['condition'], 
            )#create the like.and get condition and comment_id from json becuse comment_like does not exist
    
    response = {
        'like_count': comment.like_count, #reade from model
        'dis_like_count':comment.dis_like_count
        }#for post response to front

    return HttpResponse(json.dumps(response), status=201)
    #return the like and dis_like count in json


@csrf_exempt    #for ignor csrf token
def create_comment(request):
    #for use ajax
    '''for time we did not have serializer.so we did not use rest_full. this is just a small rest for handel the
    create_comment when we have just two or three rest did not usual use 3MB library of restFULL we can handel that whit ajax'''
    data = json.loads(request.body)#for load data get from front
    user = request.user #get user from log in
    try:
        comment = Comment.objects.create(
            post_id=data['post_id'],
            text=data['text'],
            author=user
        )
        response = {
            'text': comment.text, #reade from model
            'dis_like_count':0,
            'like_count':0,
            'full_name':user.get_full_name()#get_full_name() is func in model we define
        }#cuse we donot have serializer hier we should handel that manualy
        return HttpResponse(json.dumps(response), status=201)
        
    except:
        response = {
            'error': 'bad request error' #
            }#for post response to front
        return HttpResponse(json.dumps(response), status=404)


#def like_comment(request, post_pk):#for use refresh type
#    if request.method == 'POST':
#        print('post')
#        form = CommentLikeForm(request.POST)
#        if form.is_valid():
#            print('valid')
#            condition = form.cleaned_data['condition']
#            comment_id = form.cleaned_data['comment']
#            try:
#                print(bool(condition))
#                comment_like = CommentLike.objects.get(author=request.user, comment_id=comment_id)
#                comment_like.condition = bool(condition)
#                comment_like.save()
#            except:
#                comment_like = CommentLike.objects.create(author=request.user, 
#                comment_id=comment_id,
#                condition=condition
#                )
#        else:
#            psrint('invalid')
#    else:
#        pass
#
#    return redirect('post_detail', post_pk)




#for permistion in function view we use decorator
#from django.contrib.auth.decorators import login_reguired, permission_required
#@login_required    #default url can change in 'setting.LOGIN_REDIRECT_URL'
#@permision_required('blog.view_post', login_url= 'login')    #for check permission required
##@permision_required('blog.view_post', raise_exception=True)
#def post_list(request): #requesst is create an oject for the view func
#    #return render(request, 'blog/post_list.html', {})
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#    context = {
#        'posts' : posts 
#        }
#    return render(request, 'blog/post_list.html', context)

#def post_edit(request, pk):
#    #if not request.user.is_authenticated:
#    #    redirect(login)
#    post = get_object_or_404(Post, pk=pk)
#    if request.method == "POST":
#        form = PostForm(request.POST, instance=post)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
#            return redirect('post_detail', pk=post.pk)
#    else:
#        form = PostForm()
#    return render (request, 'blog/post_edit.html', {'form': form})


#def post_new(request):
#    #form = PostForm()
#    if request.method =='POST':
#        form = PostForm(request.POST)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
#            return redirect('post_detail', pk=post.pk)
#    else:
#        form = PostForm()
#
#    return render(request, 'blog/post_edit.html', {'form': form})


#def post_detail(request, pk):
#    try:
#       post = Post.objects.select_related('post_setting', 'category', 'author').get(pk=pk)
#       #post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
#    except Post.DoesNotExist:
#           raise Http404('post not found')
#    print(user.has_perm('blog.delete_post')) and post.author == user:  #for user permisiton check for delete or author is the user
#       ......  #qurey for delete    
#       #post = Post.objects.get(pk=pk)
#       #post = get_object_or_404(Post, pk=pk)

#    return render(request, 'blog/post_detail.html', {'post': post})


