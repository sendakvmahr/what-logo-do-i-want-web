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
	let newImgs = JSON.parse(httpGet("/new_images?count=" + 1 + "&coord=" + avgCoord))
	let container = document.getElementById("img-container")
	container.innerHTML = ""
	for (let j = 1; j < 5; j++) {
		let key = "logo" + j;
		let node = document.createElement("img")
		node.src = "static/" + newImgs[key].filename;
		node.setAttribute("data-coord", newImgs[key].coord.toString())
		container.appendChild(node)
	}
}

function recordClickValue(img) {
	let coord = JSON.parse("[" + img.attributes["data-coord"].value + "]");
	count += 1;

	// append to coords, find new coords
}

function imageClicked(e){
	recordClickValue(e.target);
	loadNewImages(e.target);
	imgsSetOnclick();
}



var count = 0;
var avgCoord = [];
var coordinates = [];
imgsSetOnclick();