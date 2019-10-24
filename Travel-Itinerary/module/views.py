from django.shortcuts import render
from .key import key
from django.http import JsonResponse
import googlemaps

from .forms import itineraryForm

# Create your views here.

gmaps = googlemaps.Client(key=key)

def index(request):
	template_name = 'module/index.html'
	form = itineraryForm()
	context = {
		'page_title': 'Create itinerary',
		'form': form,
	}

	if request.method == 'POST':
		data = []
		data = request.POST
		#dist_matrix = gmaps.distance_matrix(origins=data, destinations=data)
		print(data)
	#jResponse = JsonResponse({'result': url})
	return render(request, template_name, context)