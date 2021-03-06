#
# Author: Stanislaw Adaszewski, 2015
#

import networkx as nx
import numpy as np
import time
import pandas as pd


def constrained_kmeans(data, demand, maxiter=None, fixedprec=1e9):

	min_ = np.min(data, axis = 0)
	max_ = np.max(data, axis = 0)


	C = np.array(data.sample(n = len(demand)))
	data = np.array(data)
	M = np.array([-1] * len(data), dtype=np.int)

	print("label awal : ")
	print(M)
	
	itercnt = 0
	while True:
		itercnt += 1
		
		print("center : ")
		print(C)
		# memberships
		g = nx.DiGraph()
		g.add_nodes_from(range(0, data.shape[0]), demand=-1) # points
		for i in range(0, len(C)):
			g.add_node(len(data) + i, demand=demand[i])
		
		# Calculating cost...
		cost = np.array([np.linalg.norm(np.tile(data.T, len(C)).T - np.tile(C, len(data)).reshape(len(C) * len(data), C.shape[1]), axis=1)])
		# Preparing data_to_C_edges...
		print("jarak :")
		print(cost)
		# print(np.tile(data.T, len(C)).T - np.tile(C, len(data)).reshape(len(C) * len(data), C.shape[1]))
		data_to_C_edges = np.concatenate((np.tile([range(0, data.shape[0])], len(C)).T, np.tile(np.array([range(data.shape[0], data.shape[0] + C.shape[0])]).T, len(data)).reshape(len(C) * len(data), 1), cost.T * fixedprec), axis=1).astype(np.uint64)
		# Adding to graph
		g.add_weighted_edges_from(data_to_C_edges)
		# print("data to edge :")
		# print(data_to_C_edges)
		

		a = len(data) + len(C)
		g.add_node(a, demand=len(data)-np.sum(demand))
		C_to_a_edges = np.concatenate((np.array([range(len(data), len(data) + len(C))]).T, np.tile([[a]], len(C)).T), axis=1)
		g.add_edges_from(C_to_a_edges)
		
		
		# Calculating min cost flow...
		f = nx.min_cost_flow(g)
		print("min cost flow")
		print(f)
		
		# assign
		M_new = np.ones(len(data), dtype=np.int) * -1
		for i in range(len(data)):
			p = sorted(f[i].items(), key=lambda x: x[1])[-1][0]
			M_new[i] = p - len(data)

		print("label : ")
		print(M_new)
		# stop condition
		if np.all(M_new == M):
			# Stop
			return (C, M, f)
			
		M = M_new
			
		# compute new centers
		for i in range(len(C)):
			C[i, :] = np.mean(data[M==i, :], axis=0)
			
		if maxiter is not None and itercnt >= maxiter:
			# Max iterations reached
			return (C, M, f)