//Bugs to fix: 
// -If the user selects and deselects the layers too quickly, the layers will still load into the map

//declaring global variables
var l7Overlay;
var l8Overlay;
EE_URL = 'https://earthengine.googleapis.com';

function showData(data){
	console.log('MapID: ' + data.eeMapId);
	console.log('Token: ' + data.eeToken);
	var eeMapOptions = {
		getTileUrl: function(tile, zoom) {
			var url = EE_URL + '/map/';
			url += [data.eeMapId, zoom, tile.x, tile.y].join('/');
			url += '?token=' + data.eeToken;
			return url;
		},
		tileSize: new google.maps.Size(256, 256)
	};

	if (data.mapLayer === 'l7'){
		l7Overlay = new google.maps.ImageMapType(eeMapOptions);
		map.overlayMapTypes.setAt(0, l7Overlay);
	}else if (data.mapLayer === 'l8'){
		l8Overlay = new google.maps.ImageMapType(eeMapOptions);
		map.overlayMapTypes.setAt(1, l8Overlay);
	}
	
	//var mapType = new google.maps.ImageMapType(eeMapOptions);
	//map.overlayMapTypes.push(mapType);
}

function getLayer(){
	var l7_state = document.getElementById("formCheck-1").checked;
	var l8_state = document.getElementById("formCheck-2").checked;
	var ndvi_state = document.getElementById("formCheck-3").checked;
	var kc_state = document.getElementById("formCheck-4").checked;
	var etc_state = document.getElementById("formCheck-5").checked;
	if (l8_state === true){
		if (l8Overlay == null){
			console.log('l8 layer is null');
		}else{
			map.overlayMapTypes.removeAt(1, l8Overlay);
		}
		sendValue('l8');
	}else{
		//remove l8 overlay
		map.overlayMapTypes.removeAt(1, l8Overlay);
	}
	if (l7_state === true){
		if (l7Overlay == null){
			console.log('l7 layer is null');
		}else{
			map.overlayMapTypes.removeAt(0, l7Overlay);
		}
		sendValue('l7');
	}else{
		//remove l7 overlay
		map.overlayMapTypes.removeAt(0, l7Overlay);
	}
}

// Obtain dates
function selected_date(){
	var dateIndex = document.getElementById("select-date");
	var dateText = dateIndex.options[dateIndex.selectedIndex].text;
	var s_date = new Date(dateText);
	var s_date_string = s_date.toISOString().substring(0, 10);
	
	return s_date_string;
}

function selected_date_range(range){
	var temp_date = new Date(selected_date());
	temp_date.setDate(temp_date.getDate()-range);
	var previous_date = temp_date.toISOString().substring(0, 10);
	return(previous_date);
}

function sendValue(state) {
	console.log('Date from JavaScript: ' + selected_date());
	console.log('Date Range from JavaScript: ' + selected_date_range(128));
	console.log('Layer Requested: ' + state);
	$.ajax('/',{
		type: 'GET',
		data:{
			fmt: 'json',
			mapLayer: state,
			date: selected_date(),
			date_range: selected_date_range(128)
		},
		success: showData
	});
}

$(document).ready(function(){
	$('#formCheck-1').on('click', getLayer);
	$('#formCheck-2').on('click', getLayer);
});
document.getElementById("select-date").onchange = function(){
    getLayer();
};

/* document.getElementById("formCheck-2").addEventListener("click", checkSelection);
document.getElementById("formCheck-3").addEventListener("click", checkSelection);
document.getElementById("formCheck-4").addEventListener("click", checkSelection);
document.getElementById("formCheck-5").addEventListener("click", checkSelection); */

