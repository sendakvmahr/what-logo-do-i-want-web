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
		results = {}
		for l in lines:
			fields = l.split("\t")
			results[int(fields[0])] = (fields[1].strip(), fields[2].strip())
		return results

# More for reference than for use
def predict(data_i):
	return CLUSTER.predict([DATA[i]])

def get_logo_arguments(logo_id):
	return list(DATA[logo_id])

DATA = load_pickle("clustering/data.pickle")
CLUSTER = load_pickle("clustering/cluster_algo.pickle")
NUM_LOGOS = DATA.shape[0]
IDS = load_ids()