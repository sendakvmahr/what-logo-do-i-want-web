from flask import Flask, request, jsonify
from flask import render_template
import random
import clustering.cluster as cluster
#from flask_cors import CORS
#

#reminder for me to remove them
exclude_list = [
1176,	# teamviewer
6536,    #merrell_(company)
2199, 	#pukka_herbs
4291, 	#badedas
1479,	#broughton_foods_company
1926, 	#killer_shake
4639,	#moka_pot
]
num_logos_show = 20
num_closest_logos = 5
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

def average_id_coords(ids):
	ids = [cluster.DATA[i] for i in ids]
	result = []
	rows = len(ids)
	columns = len(ids[0])
	for y in range(columns):
		total = 0
		for x in range(rows):
			total += ids[x][y]
		result.append(total/rows)
	return result

def random_logos(n, exclude=[]):
	"""Selects multiple logos without dupelications and with exclusions """
	result = []
	for i in range(n):
		logo = random_logo(exclude)
		exclude.append(logo["id"])
		result.append(logo)
	return result

def load_cluster_images(cluster_id, exclude=[]):
	"""Given cluster ID, returns the images of logos in that cluster"""
	exclude += exclude_list
	ids_ = cluster.CLUSTERS[cluster_id]
	result = []
	for i in ids_:
		if i not in exclude:
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
	ids = request.args.get('ids').split(",")
	ids = [int(i) for i in ids]
	clusters = [cluster.id_to_cluster(i) for i in ids]
	final_average = average_id_coords(ids)
	final_cluster = -1
	for id_ in clusters:
		if clusters.count(id_) >= int(len(clusters) * .3):
			clusters = id_
	if final_cluster == -1:
		final_cluster = cluster.predict_coord(final_average)
	closest_logos = cluster.closest_logos(final_average, 3)
	return "/results?cluster={}&id={}&chosen={}".format(final_cluster, strip_list(closest_logos), request.args.get('ids'))

# TODO - descriptions of each cluster, parse ids of the 3 closest logos in url
@app.route("/results")
def results():
	chosen_logos = request.args.get('chosen').split(",")
	remove_from_cluster_ids = [int(i) for i in chosen_logos]
	chosen_logos = [logo_id_to_image(int(i)) for i in chosen_logos]

	cluster_id = int(request.args.get('cluster'))
	closest_logos = request.args.get('id').split(",")
	remove_from_cluster_ids += [int(i) for i in closest_logos]
	closest_logos = [logo_id_to_image(int(i)) for i in closest_logos]
	cluster_logos = load_cluster_images(cluster_id, remove_from_cluster_ids)
	return render_template("results.html",	
		chosen_logos=chosen_logos,
		closest_logos=closest_logos,
		cluster_logos=cluster_logos,
		cluster_id=cluster_id
		)

@app.route("/start")
def start():
	logos = random_logos(num_logos_show) 
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
	logos = random_logos(num_logos_show, exclude)
	return jsonify(logos)