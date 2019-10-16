from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views
from .views import loginView, logoutView
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
    path('register/', user_views.Users.as_view(), name='register'),
    url(r'^$', views.home, name='home'),
    path('itinerary/', views.itinerary),
]
