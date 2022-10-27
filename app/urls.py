from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map', views.map, name='map'),
    path('post', views.post, name='post'),
    path('profile', views.profile, name='profile'),
    path('profile/registration', views.registration, name='registration'),
    path('profile/logout', views.logoutUser, name='logout'),
    path('profile/login', views.loginUser, name='login'),
    path('profile/registration/districts/<int:id>', views.getdistricts, name='districts'),
    path('profile/registration/cities/<int:id>', views.getcities, name='cities')
]