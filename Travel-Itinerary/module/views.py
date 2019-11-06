from django.shortcuts import render, redirect
from .key import key
from django.views import View
import pandas as pd, time, random, numpy as np, operator, googlemaps, threading, concurrent.futures
from .ga import ga
from .kmeans import clustering

# Create your views here.

gmaps = googlemaps.Client(key=key)

def index(request):
	template_name = 'module/index.html'
	context = {
		'page_title': 'Create itinerary',
	}

	if request.method == 'POST':
		# nonlocal distMatrice
		start_time = time.time()
		template_name = 'module/result.html'
		data = request.POST
		nclusters = int(request.POST['days'])
		dataCopy = data.copy()
		list_addr = dataCopy.pop('origin')

		distance_val = []
		distances = gmaps.distance_matrix(origins=list_addr, destinations=list_addr)

		#create distance matrice
		for i in distances['rows']:
			for j in i['elements']:
				distance_val.append(j['distance']['value'])
				
		darr = split(distance_val, len(list_addr))
		distMatrice = pd.DataFrame(darr, index=list_addr, columns=list_addr)
		print(distMatrice)

		#initialize genetic algorithm & k-means class
		GA = ga(distMatrice)
		cluster = clustering(list_addr, nclusters)
		route = cluster.kmeans()

		if list_addr is not None:
			#return the route and final distance for each route
			thread1 = GA
			thread2 = cluster
			itinerary_wisata = {}
			# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			for i in range(0, nclusters):
				itinerary_wisata[i+1] = GA.geneticAlgorithm(operator.itemgetter(i)(route))
					# itinerary_wisata = executor.submit(GA.geneticAlgorithm, operator.itemgetter(i)(route))
			# thread1.start()
			# thread2.start()	
			# thread1.join()
			# thread2.join()
			print(itinerary_wisata)
			context = {
				'page_title':'Results',
				'results':itinerary_wisata,
			}

			end_time = time.time()
			print (str(end_time - start_time))
			return render(request, template_name, context)
			# return redirect('itinerary')
	
	return render(request, template_name, context)

def split(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs