from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm
from django.urls import reverse_lazy

User = get_user_model()


class RegisterUserView(generic.CreateView):
    model = User 
    form_class = UserRegisterForm
    template_name = 'auth_users/register.html'


    def get_success_url(self):
        return reverse_lazy('movie_list')
