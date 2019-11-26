from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^itinerary/', views.index, name='itinerary'),
	url(r'^unduh/', views.result, name='unduh'),
]
