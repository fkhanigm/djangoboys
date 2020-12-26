#from django.shortcuts import render, get_object_or_404, redirect
#from django.utils import timezone
from .forms import PostForm
from datetime import datetime
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import models
#from account.models import User
from django.contrib.auth import get_user_model
User = get_user_model


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(draft=False, published_date__lte=datetime.now())
    #queryset = Post.objects.all()
    ordering = ('-published_date')
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
#    template_name = 'blog/category_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context

    def get_queryset(self):
        #for filter post for each category
        return Post.objects.filter(category_id=self.kwargs.get('pk'))


class AuthorPostList(PostList):
    model = Post
    template_name = 'blog/author_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context

    def get_queryset(self):
        #for filter post for each category
        return Post.objects.filter(author_id=self.kwargs.get('pk'))




class CategoryList(ListView):
    model = Category
    template_name = 'blog/base.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context

class PostNew(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')


class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')


# Create your views here.
#def post_list(request): #requesst is create an oject for the view func
#    #return render(request, 'blog/post_list.html', {})
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#    context = {
#        'posts' : posts 
#        }
#    return render(request, 'blog/post_list.html', context)

#def post_edit(request, pk):
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
#    #post = Post.objects.get(pk=pk)
#    post = get_object_or_404(Post, pk=pk)
#    return render(request, 'blog/post_detail.html', {'post': post})


