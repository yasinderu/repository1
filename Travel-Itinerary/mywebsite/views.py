from django.shortcuts import render

def home(request):
	return render(request, 'home.html')

def itinerary(request):
	return render(request, 'Itinerary.html')