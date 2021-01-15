from flask import Flask, request, jsonify
from flask import render_template
import random
import clustering.cluster as cluster
#from flask_cors import CORS
#

#reminder for me to remove them
exclude_list = [
1176	# teamviewer
]

app = Flask(__name__)
#CORS(app)

def strip_list(l):
	return str(l).replace(' ', "")[1:-1]

def logo_id_to_image(logo_id):
	category, name = cluster.IDS[logo_id]
	return "logo_images/{}/{}.webp".format(category, name)

def random_logo(exclude=[]):
	"""Selects a random logo, excludes some"""
	if -1 not in exclude:
		exclude.append(-1)
	exclude += exclude_list
	logo_id = -1
	while logo_id in exclude:
		logo_id = random.randint(0, cluster.NUM_LOGOS)
	return {
		"filename": logo_id_to_image(logo_id),
		"coord": strip_list(cluster.get_logo_arguments(logo_id)),
		"id": logo_id
	}

def random_logos(n, exclude=[]):
	"""Selects multiple logos without dupelications and with exclusions """
	result = []
	for i in range(n):
		logo = random_logo(exclude)
		exclude.append(logo["id"])
		result.append(logo)
	return result

def load_cluster_images(cluster_id):
	"""Given cluster ID, returns the images of logos in that cluster"""
	ids_ = cluster.CLUSTERS[cluster_id]
	result = []
	for i in ids_:
		result.append(logo_id_to_image(i))
	return result

@app.route("/")
def index():
	return render_template("index.html")

#unused atm, may not be doable unless I dump the whole pipeline in the backend
@app.route("/presets")
def presets():
	return render_template("presets.html")

@app.route("/process")
def process():
	return render_template("process.html")

# TODO - include IDs of the 3 closest logos in the url
@app.route("/get_final_url")
def get_final_url():
	"""Dumping the coordinate in the url is too fat"""
	final_average = request.args.get('coord').split(",")
	final_average = [float(i) for i in final_average]
	cluster_id = cluster.predict_coord(final_average)
	return ("/results?cluster={}".format(cluster_id))

# TODO - descriptions of each cluster, parse ids of the 3 closest logos in url
@app.route("/results")
def results():
	cluster_id = int(request.args.get('cluster'))
	images = load_cluster_images(cluster_id)
	closest_logos = images[:3]
	cluster_logos = images[3:]
	return render_template("results.html",	
		closest_logos=closest_logos,
		cluster_logos=cluster_logos,
		cluster_id=cluster_id
		)

@app.route("/start")
def start():
	logos = random_logos(6) 
	return render_template(
		'start.html',
		count=0,
		logos=logos
	)

# TODO - smarter guesses on which logos should go next after 
@app.route("/new_images") 
def get_images():
	exclude = request.args.get('ids').split(",")
	# if num f ids > some number, start doing half random, half closest
	exclude = [int(x) for x in exclude]
	count = len(exclude)
	logos = random_logos(6, exclude)
	return jsonify(logos)