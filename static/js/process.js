function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function imgsSetOnclick() {
	let imgs = document.getElementsByTagName("img");
	for (let i = 0; i < imgs.length; i++) {	
		imgs[i].onclick = imageClicked;
	}
}

function loadNewImages(img) {
	let newImgs = JSON.parse(httpGet("/new_images?ids=" + ids.toString()))
	let container = document.getElementById("img-container")
	container.innerHTML = ""
	for (let j = 1; j < 5; j++) {
		let key = "logo" + j;
		let node = document.createElement("img")
		node.src = "static/" + newImgs[key].filename;
		node.setAttribute("data-coord", newImgs[key].coord.toString())
		node.setAttribute("data-id", newImgs[key].id.toString())
		container.appendChild(node)
	}
}

function recordClickValue(img) {
	let coord = JSON.parse("[" + img.attributes["data-coord"].value + "]");
	ids.push(parseInt(img.attributes["data-id"].value));
	coordinates.push(coord)
	count += 1;
	// append to coords, find new coords
}

function goToResult() {
	let requestFinalURL = "/get_final_url?coord=" + avgCoord.toString();
	let finalURL = httpGet(requestFinalURL)
	window.location.href = finalURL;
}


function calculateAverage() {
	avgCoord = [];
	let numRows = coordinates.length;
	let numCols = coordinates[0].length;
	for (let y = 0; y < numCols; y++) {
		let sum = 0;
		for (let x = 0; x < numRows; x++) {
			sum += coordinates[x][y];
		}
		avgCoord.push(sum / numRows)
	}
}


function imageClicked(e){
	recordClickValue(e.target);
	if (count == 10) {
		calculateAverage();
		goToResult();
	}
	loadNewImages(e.target);
	imgsSetOnclick();
}



var count = 0;
var avgCoord = [];
var coordinates = [];
var ids = [];
imgsSetOnclick();