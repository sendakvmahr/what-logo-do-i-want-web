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
	"""
	Selects a random logo, excludes some
	"""
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
	"""
	Makes sure a duplicate doesn't appear in when selecting more than one logo 
	"""
	result = []
	for i in range(n):
		logo = random_logo(exclude)
		exclude.append(logo["id"])
		result.append(logo)
	return result

def load_cluster_images(cluster_id):
	ids_ = cluster.CLUSTERS[cluster_id]
	result = []
	for i in ids_:
		result.append(logo_id_to_image(i))
	return result

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/presets")
def presets():
	return render_template("presets.html")

@app.route("/process")
def process():
	return render_template("process.html")

@app.route("/get_final_url")
def get_final_url():
	final_average = request.args.get('coord').split(",")
	final_average = [float(i) for i in final_average]
	cluster_id = cluster.predict_coord(final_average)
	return ("/results?cluster={}".format(cluster_id))

# do last
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
	logos = random_logos(4) 
	return render_template(
		'start.html',
		count=0,
		logo1=logos[0],
		logo2=logos[1],
		logo3=logos[2],
		logo4=logos[3],
	)

#do after start
# exclude should be counted too
@app.route("/new_images") 
def get_images():
	exclude = request.args.get('ids').split(",")
	exclude = [int(x) for x in exclude]
	#count = request.args.get('count')
	#coord = request.args.get('coord').split(",")
	logos = random_logos(4, exclude)
	return jsonify({
			"logo1": logos[0],
			"logo2": logos[1],
			"logo3": logos[2],
			"logo4": logos[3]
		})
"""
# more for ref than for actual use
#localhost:5000/get_logo?logo=wertizoo
@app.route("/get_logo", methods = ['GET'])
def get_logo():
	logo_name = request.args.get('logo')
	logo_id = str(30 * len(logo_name))
	return logo_id + " " + request.args.get('nopo')
"""