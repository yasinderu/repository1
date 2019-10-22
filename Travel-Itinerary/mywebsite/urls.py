from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^login/$', loginView, name='login'),
    #url(r'^logout/$', logoutView, name='logout'),
    #path('register/', user_views.Users.as_view(), name='register'),
    url(r'^module/', include('module.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^$', views.home, name='home'),
    #path('itinerary/', views.itinerary),
]
