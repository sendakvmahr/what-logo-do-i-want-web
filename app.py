from flask import Flask, request, jsonify
from flask import render_template
import random
#from flask_cors import CORS
#

app = Flask(__name__)
#CORS(app)

logos = [
	"logo_images/esports/cloud9.webp",
	"logo_images/demoscene/butterfly jive.webp",
	"logo_images/restaurant/aberdeen_angus_steak_houses.webp",
	"logo_images/sports_clothing/aigle_(company).webp",
]

def strip_list(l):
	return str(l).replace(' ', "")[1:-1]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/presets")
def presets():
	return render_template("presets.html")

@app.route("/process")
def process():
	return render_template("process.html")

@app.route("/results")
def results():
	final_average = request.args.get('coord').split(",")
	closest_logos = [
		"logo_images/food_drink/hp_hood.webp",
		"logo_images/food_drink/vitasoy.webp",
		"logo_images/convenience_store/kum_&_go.webp"
	]
	cluster_logos = [
		"logo_images/food_drink/cielo_(water).webp",
		"logo_images/food_drink/dolly_madison.webp",
		"logo_images/food_drink/streit's.webp",
		"logo_images/food_drink/ginsters.webp",
		"logo_images/food_drink/goetze's_candy_company.webp",
		"logo_images/food_drink/rich_products.webp",
		"logo_images/food_drink/fresh_del_monte_produce.webp",
		"logo_images/food_drink/bambi_(company).webp"
	]
	return render_template("results.html",	
		closest_logos=closest_logos,
		cluster_logos=cluster_logos,
		coord=final_average
		)



@app.route("/start")
def start():
	return render_template(
		'start.html',
		count=0,
		logo1={
			"filename": random.choice(logos),
			"coord": strip_list([1, 2, 3, 4, 6, 87, 9, 84])
		},
		logo2={
			"filename": random.choice(logos),
			"coord": strip_list([1, 2, 3, 4, 6, 87, 9, 84])
		},
		logo3={
			"filename": random.choice(logos),
			"coord": strip_list([1, 2, 3, 4, 6, 87, 9, 84])
		},
		logo4={
			"filename": random.choice(logos),
			"coord": strip_list([1, 2, 3, 4, 6, 87, 9, 84])
		},
	)

@app.route("/new_images")
def get_images():
	count = request.args.get('count')
	coord = request.args.get('coord').split(",")
	return jsonify({
			"logo1":{
				"filename": random.choice(logos),
				"coord": [1, 2, 3, 4, 6, 87, 9, 84]
			},
			"logo2":{
				"filename": random.choice(logos),
				"coord": [1, 2, 3, 4, 6, 87, 9, 84]
			},
			"logo3":{
				"filename": random.choice(logos),
				"coord": [1, 2, 3, 4, 6, 87, 9, 84]
			},
			"logo4":{
				"filename": random.choice(logos),
				"coord": [1, 2, 3, 4, 6, 87, 9, 84]
			}
		})

#localhost:5000/get_logo?logo=wertizoo
@app.route("/get_logo", methods = ['GET'])
def get_logo():
	logo_name = request.args.get('logo')
	logo_id = str(30 * len(logo_name))
	return logo_id + " " + request.args.get('nopo')
