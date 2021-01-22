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

function showLoader() {
	
	let loader = document.getElementById("loader")
	loader.classList.toggle("fade-in");
	loader.classList.toggle("fade-out");

	let container = document.getElementById("img-container");
	container.style.height = container.clientHeight + "px";
	container.classList.toggle("fade-out");
	container.classList.toggle("fade-in");
}

function hideLoader() {
	let loader = document.getElementById("loader")
	loader.classList.toggle("fade-out");
	loader.classList.toggle("fade-in");

	let container = document.getElementById("img-container");
	container.style.height = container.clientHeight + "px";
	container.classList.toggle("fade-in");
	container.classList.toggle("fade-out");
}

function loadNewImages(img) {
	showLoader();
	
	let newImgs = JSON.parse(httpGet("/new_images?ids=" + ids.toString()))
	let container = document.getElementById("img-container")
	container.innerHTML = "";
	for (let j = 0; j < newImgs.length; j++) {
		let image = newImgs[j];
		let node = document.createElement("img");
		node.src = "static/" + image.filename;
		node.setAttribute("data-coord", image.coord.toString());
		node.setAttribute("data-id", image.id.toString());
		container.appendChild(node);
	}
	
	hideLoader();
}

function recordClickValue(img) {
	let coord = JSON.parse("[" + img.attributes["data-coord"].value + "]");
	ids.push(parseInt(img.attributes["data-id"].value));
	coordinates.push(coord)
	count += 1;
	// append to coords, find new coords
}

function goToResult() {
	let requestFinalURL = "/get_final_url?ids=" + ids.toString();
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