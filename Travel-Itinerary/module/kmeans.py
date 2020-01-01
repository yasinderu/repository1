import pandas as pd, numpy as np, googlemaps
from sklearn.cluster import KMeans
from .key import key
from .constrained_kmeans import constrained_kmeans
# from sklearn.metrics import silhouette_score
import threading

gmaps = googlemaps.Client(key=key)

class clustering(threading.Thread):
	def __init__(self, list_dest, nclusters):
		threading.Thread.__init__(self)
		self.list_addr = list_dest
		self.nclusters = nclusters
		self.lat = []
		self.lng = []

		for k in list_dest:
			loc = gmaps.geocode(k)
			self.lat.append(loc[0]['geometry']['location']['lat'])
			self.lng.append(loc[0]['geometry']['location']['lng'])

	def kmeans(self):
		d = {'lat':self.lat, 'lng':self.lng}
		df = pd.DataFrame(data=d, index=self.list_addr)
		cons = int(len(self.list_addr)/self.nclusters)
		print(df)
		demand = []
		for i in range(self.nclusters):
			demand.append(cons)
		
		# if nclusters == 1:
		# 	kmeans = KMeans

		(C, M, F) = constrained_kmeans(df, demand)

		# score = silhouette_score(df, M)

		# print("silhouette_score : ")
		# print(score)

		clusters = {}
		n = 0
		for item in M:
			if item in clusters:
				clusters[item].append(self.list_addr[n])
			else:
				clusters[item] = [self.list_addr[n]]
			n+=1
		return clusters