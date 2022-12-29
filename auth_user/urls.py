from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('users/register/', views.RegisterUserView.as_view(), name='register'),
    path('users/login/', auth_views.LoginView.as_view(), name='login'),
    path('users/logout/', auth_views.LogoutView.as_view(), name='logout')

]