import numpy as np, pandas as pd, googlemaps, operator, random, time
from .key import key
import threading, concurrent.futures

gmaps = googlemaps.Client(key=key)

class ga():
	def __init__(self, population, origin):
		self.population = population
		self.distance_val = []
		self.durations = []
		self.origin = origin
		self.popSize = 50
		self.eliteSize = 20
		self.mutationRate = 0.01
		self.generations = 50
		# self._return = None

		def split(arr, size):
			arrs = []
			while len(arr) > size:
				pice = arr[:size]
				arrs.append(pice)
				arr = arr[size:]
			arrs.append(arr)
			return arrs

		self.population.insert(0, self.origin)
		self.response = gmaps.distance_matrix(origins=self.population, destinations=self.population)

		for i in self.response['rows']:
			for j in i['elements']:
				self.distance_val.append(j['distance']['value'])
				self.durations.append(j['duration']['value'])

		self.durArr = split(self.durations, len(self.population))
		self.distArr = split(self.distance_val, len(self.population))

		self.distMatrice = pd.DataFrame(self.distArr, index=self.population, columns=self.population)
		self.durMatrice = pd.DataFrame(self.durArr, index=self.population, columns=self.population)

	# def join(self, *args):
	# 	threading.Thread.join(self, *args)
	# 	return self._return

	def getDistance(self, fromCity, toCity):
		distance = self.distMatrice[fromCity][toCity]
		return distance

	def getDuration(self, route):
		duration = 0
		for i in range(0, len(route)):
			fromCity = route[i]
			toCity = None
			if i + 1 < len(route):
				toCity = route[i + 1]
			else:
				toCity = route[i]
			duration += self.durMatrice[fromCity][toCity] + 7200
			print(duration)
			# durr = duration + 120
		if int(duration/3600) > 1:
			totalDuration = int(duration/3600), 'Jam', int(duration%3600/60), 'Menit'
		else:
			totalDuration = int(duration/60), 'Menit'
		return totalDuration

	def routeDistance(self, route):
		routeDistance = 0
		threadss = []
		for i in range(0, len(route)):
			fromCity = route[i]
			toCity = None
			if i + 1 < len(route):
				toCity = route[i + 1]
			else:
				toCity = route[i]
			routeDistance += self.getDistance(fromCity, toCity)
		totalDistance = routeDistance
		return totalDistance

	def routeFitness(self, route):
		if len(route) == 1:
			fitness = 1
		else:
			fitness = 1 / float(self.routeDistance(route))
		return fitness

	def createRoute(self, population):
		route = random.sample(population, len(population))
		route.insert(0, self.origin)
		return route

	def initialPopulation(self, populations):
		population = []

		for i in range(0, self.popSize):
			population.append(self.createRoute(populations))
		return population

	def rankRoutes(self, currentGen):
		fitnessResults = {}
		for i in range(0, len(currentGen)):
			fitnessResults[i] = self.routeFitness(currentGen[i])
		sorteds = sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse=True)
		# print(sorteds)
		return sorteds

	def selection(self, popRanked):
		selectionResults = []
		df = pd.DataFrame(np.array(popRanked), columns=["index", "Fitness"])
		df['cum_sum'] = df.Fitness.cumsum()
		df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

		for i in range(0, self.eliteSize):
			selectionResults.append(popRanked[i][0])
		for i in range(0, len(popRanked) - self.eliteSize):
			pick = 100*random.random()
			for i in range(0, len(popRanked)):
				if pick <= df.iat[i,3]:
					selectionResults.append(popRanked[i][0])
					break
		return selectionResults

	def matingPool(self, currentGen, selectionResults):
		matingpool = []
		for i in range(0, len(selectionResults)):
			index = selectionResults[i]
			matingpool.append(currentGen[index])
		return matingpool

	def breed(self, parent1, parent2):
		child = []
		childP1 = []
		childP2 = []

		geneA = int(random.random()*len(parent1))
		geneB = int(random.random()*len(parent1))

		startGene = min(geneA, geneB)
		endGene = max(geneA, geneB)

		if startGene == 0:
			startGene += 1

		for i in range(startGene, endGene):
			childP1.append(parent1[i])

		childP2 = [item for item in parent2 if item not in childP1]

		child = childP2 + childP1
		return child

	def breedPopulation(self, matingpool):
		children = []
		length = len(matingpool) - self.eliteSize
		pool = random.sample(matingpool, len(matingpool))

		# print(pool)
		for i in range(0, self.eliteSize):
			children.append(matingpool[i])

		for i in range(0, length):
			child = self.breed(pool[i], pool[len(matingpool)-i-1])
			children.append(child)
		# print(children)
		return children

	def mutate(self, individual):
		for swapped in range(1, len(individual)):
			if (random.random() <= self.mutationRate):
				swapWith = int(random.random()*len(individual))
				if swapWith == 0:
					swapWith += 1

				city1 = individual[swapped]
				city2 = individual[swapWith]

				individual[swapped] = city2
				individual[swapWith] = city1
		return individual

	def mutatePopulation(self, children):
		mutatedPop = []

		for ind in range(0, len(children)):
			mutatedInd = self.mutate(children[ind])
			mutatedPop.append(mutatedInd)
		return mutatedPop

	def nextGeneration(self, currentGen):
		popRanked = self.rankRoutes(currentGen)
		selectionResults = self.selection(popRanked)
		matingpool = self.matingPool(currentGen, selectionResults)
		children = self.breedPopulation(matingpool)
		nextGeneration = self.mutatePopulation(children)
		return nextGeneration

	def geneticAlgorithm(self):
		start_time = time.time()
		lat = []
		lng = []
		place_id = []
		place_url = []
		population = self.population[1:len(self.population)]
		pops = self.initialPopulation(population)
		for i in range(0, self.generations):
			pops = self.nextGeneration(pops)
		final_distance = float(1/self.rankRoutes(pops)[0][1]) / 1000
		bestRouteIndex = self.rankRoutes(pops)[0][0]
		bestRoute = pops[bestRouteIndex]

		for item in bestRoute:
			loc = gmaps.geocode(item)
			lat.append(loc[0]['geometry']['location']['lat'])
			lng.append(loc[0]['geometry']['location']['lng'])
			place_id.append(loc[0]['place_id'])

		duration = self.getDuration(bestRoute)
		detail = list(zip(bestRoute, lat, lng, place_id))

		dist = []
		for i in range(0, len(bestRoute)-1):
			fromCity = bestRoute[i]
			toCity = None
			if i + 1 < len(bestRoute):
				toCity = bestRoute[i + 1]
			else:
				toCity = bestRoute[i]
			dist.append(self.getDistance(fromCity, toCity))

		result = {'routes': bestRoute, 'dist': dist, 'addr':detail, 'lat': lat, 'lng': lng, 'distance': int(final_distance), 'duration': duration}
		end_time = time.time()
		print("Best route : " + str(bestRoute))
		print("Distance : " + str(final_distance))
		print("Running Time : " + str(end_time - start_time))
		print(result)
		return result