import numpy as np
import pickle
from sklearn.cluster import KMeans
# This whole module should be more communicating with a database 
# but I don't think a database is part of the payment

def load_pickle(file):
	with open(file, "rb") as f: 
		return pickle.load(f)

def load_ids():
	"""
	slightly different loading atm because I have a feeling some special 
	characters will be a headache and I will have to go through
	them manually later in the process
	"""
	with open("clustering/ids.txt", "r") as f:
		lines = f.readlines()
		ids = {}
		by_cluster = {}
		for i in range(65): #I just know there's 65 clusters 
			by_cluster[i] = []
		for l in lines:
			fields = l.split("\t")
			id_ = int(fields[0])
			ids[id_] = (fields[2].strip(), fields[1].strip())
			by_cluster[int(fields[3])].append(id_)
		return ids, by_cluster

# More for reference than for use
def predict(data_i):
	return CLUSTER.predict([DATA[i]])

def predict_coord(coord):
	return CLUSTER.predict([coord])[0]

def get_logo_arguments(logo_id):
	return list(DATA[logo_id])

DATA = load_pickle("clustering/data.pickle")
CLUSTER = load_pickle("clustering/cluster_algo.pickle")
NUM_LOGOS = DATA.shape[0]
IDS, CLUSTERS = load_ids()