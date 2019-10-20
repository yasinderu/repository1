from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^register/$', views.Users.as_view(), name='register'),
	url(r'^login/$', views.loginView, name='login'),
	url(r'^logout/$', views.logoutView, name='logout'),
	url(r'^profile/$', views.view_profile, name='view_profile'),
	url(r'^profile/edit/', views.edit_profile, name='edit_profile'), 
]