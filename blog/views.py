from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm 
from django.contrib.auth import get_user_model
User = get_user_model()
#this func is instead we give them the srt "settings.AUTH_USER_MODEL" or "account.User"is going to find the right function and give that hear
#in views, forms, admin and anoder risivers data files we should use this func instead give the 'stu'


# Create your views here.
def post_list(request): #requesst is create an oject for the view func
    #return render(request, 'blog/post_list.html', {})
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {
        'posts' : posts 
        }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
#   form = PostForm()
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render (request, 'blog/post_edit.html', {'form': form})

def register_user(request):
    if request.method == 'POST' :
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #avatar =  
            full_name = form.cleaned_data['full_name']
            User.objects.create_user(password=password, email=email, full_name=full_name)

            return redirect('post_list')

        else:
            pass
        context = {'form': form}
    else:
        form = UserRegistrationForm()
        context = {'form': form}

    return render(request, 'bog/register.html', context=context)