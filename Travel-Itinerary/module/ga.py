import numpy as np, pandas as pd, googlemaps, operator, random, time
from .key import key
import threading, concurrent.futures

gmaps = googlemaps.Client(key=key)

class ga(threading.Thread):
	def __init__(self, distMatrice, durMatrice):
		threading.Thread.__init__(self)
		self.distMatrice = distMatrice
		self.durMatrice = durMatrice
		self.distance_val = []
		self.popSize = 50
		self.eliteSize = 20
		self.mutationRate = 0.01
		self.generations = 50

	def getDistance(self, fromCity, toCity):
		#locks.acquire()
		distance = self.distMatrice[fromCity][toCity]
		#locks.release()
		return distance

	def getDuration(self, route):
		duration = 0
		for i in range(0, len(route)):
			fromCity = route[i]
			toCity = None
			if i + 1 < len(route):
				toCity = route[i + 1]
			else:
				toCity = route[0]
			duration += self.durMatrice[fromCity][toCity]
		if duration/3600 > 1:
			totalDuration = int(duration/3600), 'Jam', int(duration%3600)/60, 'Menit'
		else:
			totalDuration = int(duration/60), 'Menit'
		# totalDuration = duration	
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
				toCity = route[0]
			# thread2 = threading.Thread(target=self.getDistance, args=(fromCity, toCity),)
			routeDistance += self.getDistance(fromCity, toCity)
			# thread2.start()
		totalDistance = routeDistance
		return totalDistance

	def routeFitness(self, route):
		# t1 = threading.Thread(target = self.routeDistance, args=(route))
		# t1.start()
		# lock.acquire()
		if len(route) == 1:
			fitness = 1
		else:
			fitness = 1 / float(self.routeDistance(route))
		# lock.release()
		# t1.join()
		return fitness

	def createRoute(self, population):
		route = random.sample(population, len(population))
		return route

	def initialPopulation(self, populations):
		population = []

		for i in range(0, self.popSize):
			population.append(self.createRoute(populations))
		return population

	def rankRoutes(self, currentGen):
		fitnessResults = {}
		# threads = []
		# lock = threading.Lock()
		# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		for i in range(0, len(currentGen)):
				# fitnessResult = executor.submit(self.routeFitness, currentGen[i])
		# 	t1 = threading.Thread(target = self.routeFitness, args=(lock, currentGen[i]))
		# 	t1.start()
		# 	threads.append(t1)
			fitnessResults[i] = self.routeFitness(currentGen[i])
			# thread2 = threading.Thread(target=self.routeFitness, args=[currentGen[i]])
			# thread2.start()
		# for thread in threads:
		# 	t1.join()
		sorteds = sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse=True)
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

		for i in range(startGene, endGene):
			childP1.append(parent1[i])

		childP2 = [item for item in parent2 if item not in childP1]

		child = childP1 + childP2
		return child

	def breedPopulation(self, matingpool):
		children = []
		length = len(matingpool) - self.eliteSize
		pool = random.sample(matingpool, len(matingpool))

		for i in range(0, self.eliteSize):
			children.append(matingpool[i])

		for i in range(0, length):
			child = self.breed(pool[i], pool[len(matingpool)-i-1])
			children.append(child)
		return children

	def mutate(self, individual):
		for swapped in range(len(individual)):
			if (random.random() <= self.mutationRate):
				swapWith = int(random.random()*len(individual))

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
		# lock.acquire()
		with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			popRanked = executor.submit(self.rankRoutes(currentGen))
		popRanked = self.rankRoutes(currentGen)
		selectionResults = self.selection(popRanked)
		matingpool = self.matingPool(currentGen, selectionResults)
		children = self.breedPopulation(matingpool)
		nextGeneration = self.mutatePopulation(children)
		# lock.release()
		return nextGeneration

	def geneticAlgorithm(self, population):
		start_time = time.time()
		pops = self.initialPopulation(population)
		# lock = threading.Lock()
		# threads = []
		for i in range(0, self.generations):
			pops = self.nextGeneration(pops)
			# thread1 = threading.Thread(target=self.nextGeneration, args=[pops])
			# thread1.start()
			# pops = threading.Thread(target=self.nextGeneration(pops))
		# 	t2 = threading.Thread(target=self.nextGeneration, args=(pops))
		# 	t2.start()
		# 	threads.append(t2)
		# for thread in threads:
		# 	t2.join()
		final_distance = float(1/self.rankRoutes(pops)[0][1]) / 1000
		bestRouteIndex = self.rankRoutes(pops)[0][0]
		bestRoute = pops[bestRouteIndex]
		duration = self.getDuration(bestRoute)
		result = {'routes':bestRoute, 'distance': final_distance, 'duration': duration}
		end_time = time.time()
		print("Best route : " + str(bestRoute))
		print("Distance : " + str(final_distance))
		print("Running Time : " + str(end_time - start_time))
		# return bestRoute, final_distance
		return result