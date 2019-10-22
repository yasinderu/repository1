from django.shortcuts import render
from .key import key
from django.http import JsonResponse

# Create your views here.

search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
detail_url = "https://maps.googleapis.com/maps/api/place/details/json"

def index(request):
	template_name = 'module/index.html'
	context = {
		'page_title': 'Create itinerary'
	}
	url = "https://www.google.com"
	print(request)
	#jResponse = JsonResponse({'result': url})
	return render(request, template_name, context)


def search(request):

	url = "https://www.google.com"
	print(request)
	jResponse = JsonResponse({'result': url})
	return jResponse