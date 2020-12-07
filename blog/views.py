from django.shortcuts import render

# Create your views here.
def post_list(request): #requesst is create an oject for the view func
    return render(request, 'blog/post_list.html', {})