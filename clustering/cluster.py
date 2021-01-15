import numpy as np
import pickle
from sklearn.cluster import KMeans

def load_pickle(file):
	with open(file, "rb") as f: 
		return pickle.load(f)


DATA = load_pickle("data.pickle")
CLUSTER = load_pickle("cluster_algo.pickle")