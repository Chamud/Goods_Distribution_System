from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<int:city>', views.homefiltered, name='home'),
    path('search/<str:search>', views.homesearch, name='home'),
    path('map', views.map, name='map'),
    path('review/<int:points>/<int:info>', views.review, name='review'),
    path('post/<int:typ>/<int:id>', views.post, name='post'),
    path('deletepost/<int:id>', views.deletepost, name='deletepost'),
    path('profile', views.getprofile, name='getprofile'),
    path('items/<int:id>', views.items, name='items'),
    path('filter/services/<int:city>', views.filtservices, name='services'),
    path('filter/items/<int:city>', views.filtitems, name='items'),
    path('services/<int:id>', views.services, name='services'),
    path('profile/registration', views.registration, name='registration'),
    path('profile/logout', views.logoutUser, name='logout'),
    path('profile/login', views.loginUser, name='login'),
    path('profile/registration/districts/<int:id>', views.getdistricts, name='districts'),
    path('profile/registration/cities/<int:id>', views.getcities, name='cities'),
    #path('bycity/<int:id>', views.filteredInfo, name='bycity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)