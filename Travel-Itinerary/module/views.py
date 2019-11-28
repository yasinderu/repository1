from django.shortcuts import render, redirect
from django.contrib import messages
from .key import key
from django.views import View
import pandas as pd, time, random, numpy as np, operator, googlemaps, threading, concurrent.futures
from .ga import ga
from .kmeans import clustering
import json

# Create your views here.

gmaps = googlemaps.Client(key=key)

def index(request):
	template_name = 'module/index1.html'
	context = {
		'page_title': 'Create Itinerary',
	}

	if request.method == 'POST':
		# nonlocal distMatrice
		start_time = time.time()
		template_name = 'module/result.html'
		data = request.POST
		nclusters = int(request.POST['days'])
		dataCopy = data.copy()
		origin = request.POST['origin']
		list_addr = dataCopy.pop('destination')

		if len(list_addr) <= nclusters:
			messages.error(request, 'Jumlah destinasi tidak boleh kurang dari jumlah hari')
			return redirect('itinerary')

		cluster = clustering(list_addr, nclusters)
		route = cluster.kmeans()
		list_addr.insert(0, origin)
		# list_addrM = ['candi prambanan','istana ratu boko','gembira loka zoo','kraton yogyakarta','malioboro yogyakarta','benteng vredeburg','candi mendut','candi borobudur','sindu kusuma edupark','jogja bay waterpark','Taman Sari, Patehan, Yogyakarta City, Special Region of Yogyakarta, Indonesia','alun alun kidul yogyakarta','taman pelangi jogja','taman pintar yogyakarta','pasar beringharjo yogyakarta','tebing breksi','museum gunungapi merapi','hutan pinus pengger','puncak becici','bukit paralayang watugupit']

		distance_val = []
		durations = []
		response = gmaps.distance_matrix(origins=list_addr, destinations=list_addr)

		#create distance matrice
		for i in response['rows']:
			for j in i['elements']:
				distance_val.append(j['distance']['value'])
				durations.append(j['duration']['value'])
		# distance_val = [0, 5586, 14328, 18334, 16804, 17659, 49160, 51512, 18394, 13423, 20286, 19821, 19339, 17592, 17483, 7004, 24010, 18664, 23408, 46930, 5517, 0, 14519, 18525, 16995, 17850, 49351, 51704, 18586, 13345, 20477, 20012, 19530, 17783, 17674, 3490, 28602, 16545, 21290, 47908, 14258, 14654, 0, 4442, 5524, 4380, 40508, 42860, 8320, 10931, 5778, 5313, 10761, 3699, 6204, 15812, 27651, 17906, 19978, 34955, 18145, 18542, 4323, 0, 2674, 1802, 37981, 41754, 5793, 11454, 1121, 1322, 8235, 909, 3354, 19700, 26405, 21201, 22235, 29735, 17210, 17606, 4518, 1506, 0, 855, 36743, 39095, 4555, 10825, 2617, 2818, 6996, 1329, 680, 18764, 25166, 22414, 23188, 30687, 17865, 18261, 4042, 651, 2394, 0, 37586, 41358, 5397, 11173, 1761, 1962, 7839, 474, 3073, 19419, 26009, 21408, 22442, 29942, 46739, 48258, 39527, 36508, 35510, 36366, 0, 3995, 34041, 35394, 37028, 37230, 30054, 36656, 36190, 49416, 33278, 57067, 61316, 65652, 50382, 51901, 43170, 41432, 39153, 40008, 3996, 0, 37684, 39037, 41952, 42153, 33697, 41544, 39833, 53059, 36921, 62150, 63184, 67519, 18907, 19304, 8653, 5634, 4637, 5492, 34205, 36557, 0, 12567, 6155, 6356, 5428, 5782, 5316, 20462, 23599, 27361, 33975, 40988, 13924, 14321, 11075, 15081, 10458, 11314, 36608, 38960, 12530, 0, 17033, 16568, 8582, 14339, 11138, 15479, 18020, 24853, 28700, 43677, 20116, 20513, 5990, 1196, 3921, 2895, 38216, 41971, 6027, 12701, 0, 473, 8469, 2002, 4601, 21671, 26639, 20982, 22016, 29456, 19643, 20039, 5516, 1397, 3660, 2838, 38417, 42172, 6228, 12439, 465, 0, 8670, 2157, 4340, 21197, 26840, 20508, 21542, 28982, 18182, 18579, 9959, 7831, 5943, 6798, 32583, 34935, 6710, 7513, 8852, 8822, 0, 7089, 6623, 19737, 18545, 27387, 29459, 36115, 17522, 17918, 3699, 873, 2050, 745, 37808, 41581, 5620, 10830, 1984, 2185, 8061, 0, 2730, 19076, 24808, 21065, 22099, 29599, 17215, 17611, 4218, 826, 2050, 176, 37185, 39537, 4997, 10830, 1937, 2138, 7438, 650, 0, 18769, 25608, 21584, 22618, 30117, 6936, 3490, 15677, 19683, 18153, 19008, 50509, 52861, 19743, 14503, 21635, 21170, 20688, 18941, 18832, 0, 30021, 16879, 21624, 48242, 24239, 28780, 27794, 25758, 23233, 24089, 34854, 37206, 23291, 18047, 26278, 26479, 19304, 24379, 23913, 30199, 0, 39726, 44470, 60863, 18596, 16545, 17906, 20837, 23430, 22286, 59414, 61767, 26728, 25374, 20397, 19932, 29593, 21605, 24110, 16879, 39575, 0, 4745, 35682, 23340, 21290, 19520, 21871, 22652, 22404, 63616, 62948, 28342, 30119, 21431, 20966, 35610, 21724, 23332, 21624, 44320, 4745, 0, 30988, 46839, 47639, 32187, 29731, 31086, 30264, 66266, 68182, 34581, 43512, 29245, 28780, 42962, 29583, 31766, 47973, 61132, 36884, 31593, 0]
		# darr = split(distance_val, len(list_addrM))
		durArr = split(durations, len(list_addr))
		distArr = split(distance_val, len(list_addr))

		# distMatrice = pd.DataFrame(darr, index=list_addrM, columns=list_addrM)
		distMatrice = pd.DataFrame(distArr, index=list_addr, columns=list_addr)
		durMatrice = pd.DataFrame(durArr, index=list_addr, columns=list_addr)
		# print(darr)
		# print(distMatrice)

		#initialize genetic algorithm & k-means class
		GA = ga(distMatrice, durMatrice, origin)

		#return the route and final distance for each route
		if list_addr is not None:
			
			result = {}
			# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			for i in range(0, nclusters):
			# thread3 = threading.Thread(target=GA.geneticAlgorithm, args=(operator.itemgetter(0)(route),))
			# thread4 = threading.Thread(target=GA.geneticAlgorithm, args=(operator.itemgetter(1)(route),))
			# thread5 = threading.Thread(target=GA.geneticAlgorithm, args=(operator.itemgetter(2)(route),))
			# thread3.start()
			# thread4.start()
			# thread5.start()
			# thread3.join()
			# thread4.join()
			# thread5.join()
				result[i+1] = GA.geneticAlgorithm(operator.itemgetter(i)(route))
				# result = GA.geneticAlgorithm(operator.itemgetter(i)(route))
					# executor.submit(GA.geneticAlgorithm, operator.itemgetter(i)(route))
			# thread1.start()
			# thread2.start()	
			# thread1.join()
			# thread2.join()
			
			results = json.dumps(result)
			print(result)
			context = {
				'page_title':'Rencana Perjalanan Anda',
				'results':result,
				'result_json':results,
				# 'addr': addr
			}

			request.session['result'] = result
			request.session['result_json'] = results
			end_time = time.time()
			print (str(end_time - start_time))
			return render(request, template_name, context)
			# return redirect('itinerary')
	
	return render(request, template_name, context)

# def viewMap(request, result):
# 	pass

def result(request):
	# if request.session.has_key('result'):
	result = {}
	result = request.session['result']
	result_json = request.session['result_json']
	context = {
		'results':result,
		'result_json':result_json,
	} 
	return render(request, 'module/result2.html', context)

def split(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs