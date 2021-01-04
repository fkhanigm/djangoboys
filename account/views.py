from .forms import UserRegisterForm
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUp(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'blog/signup.html'
    success_message = 'your profile was created successfully'

class LogIn(LoginView):
    template_name = 'blog/login.html'
#    success_url = reverse_lazy('post_list')

class LogOut(LogoutView):
    template_name = 'blog/logout.html'
#    success_url = 'blog/post_list'


# Create your views here.
#def register_user(request):
#    if request.method == 'POST' :
#        form = UserRegistrationForm(request.POST)
#        if form.is_valid():
#            password = form.cleaned_data['password']
#            email = form.cleaned_data['email']
#            #avatar =  
#            full_name = form.cleaned_data['full_name']
#            User.objects.create_user(password=password, email=email, full_name=full_name)
#
#            return redirect('post_list')
#
#        else:
#            pass
#        context = {'form': form}
#    else:
#        form = UserRegistrationForm()
#        context = {'form': form}
#
#    return render(request, 'bog/register.html', context=context)