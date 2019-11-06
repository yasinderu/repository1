from django.shortcuts import render, redirect
from .key import key
from django.views import View
import googlemaps, pandas as pd, time, random, numpy as np, operator, threading
#from .ga import ga
from .kmeans import clustering
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
		start_time = time.time()
		template_name = 'module/result.html'
		data = request.POST
		nclusters = int(request.POST['days'])
		dataCopy = data.copy()
		list_addr = dataCopy.pop('origin')

		# GA = ga(list_addr)
		cluster = clustering(list_addr, nclusters)
		kmeans = cluster.kmeans()

		distance_val = []
		distances = gmaps.distance_matrix(origins=list_addr, destinations=list_addr)

		for i in distances['rows']:
			for j in i['elements']:
				distance_val.append(j['distance']['value'])
				
		darr = split(distance_val, len(list_addr))
		df = pd.DataFrame(darr, index=list_addr, columns=list_addr)
		print(df)

		if list_addr is not None:
			def getDistance(fromCity, toCity):
				distance = df[fromCity][toCity]
				return distance

			class Fitness:
				def __init__(self, route):
					self.route = route
					self.totalDistance = 0
					self.fitness = 0.0

				def routeDistance(self):
					if self.totalDistance == 0:
						routeDistance = 0
						threads = []
						for i in range(0, len(self.route)):
							fromCity = self.route[i]
							toCity = None
							if i + 1 < len(self.route):
								toCity = self.route[i + 1]
							else:
								toCity = self.route[0]
							routeDistance += getDistance(fromCity, toCity)

						self.totalDistance = routeDistance
					return self.totalDistance

				def routeFitness(self):
					if self.fitness == 0:
						threads = []
						if len(self.route) == 1:
							self.fitness = 1
						else:
							self.fitness = 1 / float(self.routeDistance())

						# for i in range(5):
						# 	t = threading.Thread(target = self.routeDistance)
						# 	threads.append(t)
						# 	t.start()

						# for thread in threads:
						# 	t.join()
					return self.fitness

			def createRoute(list_addr):
				route = random.sample(list_addr, len(list_addr))
				return route

			def initialPopulation(popSize, list_addr):
				population = []

				for i in range(0, popSize):
					population.append(createRoute(list_addr))
				return population

			def rankRoutes(population):
				fitnessResults = {}
				for i in range(0, len(population)):
					fitnessResults[i] = Fitness(population[i]).routeFitness()
				sorteds = sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse=True)
				#print(fitnessResults)
				return sorteds

			def selection(popRanked, eliteSize):
				selectionResults = []
				df = pd.DataFrame(np.array(popRanked), columns=["index", "Fitness"])
				df['cum_sum'] = df.Fitness.cumsum()
				df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

				for i in range(0, eliteSize):
					selectionResults.append(popRanked[i][0])
				for i in range(0, len(popRanked) - eliteSize):
					pick = 100*random.random()
					for i in range(0, len(popRanked)):
						if pick <= df.iat[i,3]:
							selectionResults.append(popRanked[i][0])
							break
				return selectionResults

			def matingPool(population, selectionResults):
				matingpool = []
				for i in range(0, len(selectionResults)):
					index = selectionResults[i]
					matingpool.append(population[index])
				return matingpool

			def breed(parent1, parent2):
				child = []
				childP1 = []
				childP2 = []

				geneA = int(random.random()*len(parent1))
				geneB = int(random.random()*len(parent1))

				startGene = min(geneA, geneB)
				endGene = max(geneA, geneB)

				for i in range(startGene, endGene):
					childP1.append(parent1[i])

				childP2 = [item for item in parent2 if item not in childP1]

				child = childP1 + childP2
				return child

			def breedPopulation(matingpool, eliteSize):
				children = []
				length = len(matingpool) - eliteSize
				pool = random.sample(matingpool, len(matingpool))

				for i in range(0, eliteSize):
					children.append(matingpool[i])

				for i in range(0, length):
					child = breed(pool[i], pool[len(matingpool)-i-1])
					children.append(child)
				return children

			def mutate(individual, mutationRate):
				for swapped in range(len(individual)):
					if (random.random() <= mutationRate):
						swapWith = int(random.random()*len(individual))

						city1 = individual[swapped]
						city2 = individual[swapWith]

						individual[swapped] = city2
						individual[swapWith] = city1
				return individual

			def mutatePopulation(population, mutationRate):
				mutatedPop = []

				for ind in range(0, len(population)):
					mutatedInd = mutate(population[ind], mutationRate)
					mutatedPop.append(mutatedInd)
				return mutatedPop

			def nextGeneration(currentGen, eliteSize, mutationRate):
				popRanked = rankRoutes(currentGen)
				selectionResults = selection(popRanked, eliteSize)
				matingpool = matingPool(currentGen, selectionResults)
				children = breedPopulation(matingpool, eliteSize)
				nextGeneration = mutatePopulation(children, mutationRate)
				return nextGeneration

			def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
				pops = initialPopulation(popSize, population)
				for i in range(0, generations):
					pops = nextGeneration(pops, eliteSize, mutationRate)

				print("final_distance : " + str(1/rankRoutes(pops)[0][1]))
				final_distance = float(1/rankRoutes(pops)[0][1]) / 1000
				bestRouteIndex = rankRoutes(pops)[0][0]
				bestRoute = pops[bestRouteIndex]
				result = {'routes':bestRoute, 'distance': final_distance}
				#print("Running Time : " + str(end_time - start_time))
				print(str(bestRoute))
				return bestRoute, str(final_distance)

			itinerary_wisata = {}
			for i in range(0, nclusters):
				itinerary_wisata[i+1] = geneticAlgorithm(operator.itemgetter(i)(kmeans), 
					popSize=50, eliteSize=30, mutationRate=0.01, generations=50)

			# itinerary_wisata = {}
			# for i in range(0, nclusters):
			# 	itinerary_wisata[i+1] = geneticAlgorithm(operator.itemgetter(i)(kmeans))

			print(itinerary_wisata)
			context = {
				'page_title':'Results',
				'results':itinerary_wisata,
			}

			end_time = time.time()
			print(end_time - start_time)
			# return render(request, template_name, context)
			return redirect('itinerary')
	
	return render(request, template_name, context)

def split(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs