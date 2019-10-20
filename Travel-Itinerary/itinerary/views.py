from django.shortcuts import render, redirect

# Create your views here.

def createItinerary(request):
	template_name = 'itinerary/index.html'
	context = {
		'page_title': 'ITINERARY'
	}
	return render(request, template_name, context)