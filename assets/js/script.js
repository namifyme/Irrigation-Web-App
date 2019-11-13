//namespace
basic = {};

basic.boot = function(mapKey) {
  console.log("basic.boot executed");
  // Load external libraries.
  google.load('visualization', '1.0');
  google.load('jquery', '1');
  google.load('maps', '3', {'other_params': mapKey});

  // Create the basic map app. https://developers.google.com/maps/documentation/javascript/controls
  google.setOnLoadCallback(function() {
    basic.App();
    console.log("end of map load");
  });
  
};

basic.App = function() {
	// Create and display the map.
	this.mapOptions = {
		streetViewControl: false,
		center:{lat:-34.397, lng:150.644},
		zoom:8,
		mapTypeControl: false,
		fullscreenControl: true,
		fullscreenControlOptions: {
			position: google.maps.ControlPosition.BOTTOM_RIGHT
		}
	};
	window.map = new google.maps.Map(document.getElementById('map'), this.mapOptions);
	map.setMapTypeId('hybrid');
};

basic.populate = function() {
    console.log('populate select');
    var select = document.getElementById("select-date");
    var now = new Date();
    var options = { year: 'numeric', month: 'long', day: 'numeric' };
    var timeList = [];
    for (var d = new Date(2010, 4, 1); d <= now; d.setDate(d.getDate() + 8)) {
        var dateFormatted = d.toLocaleDateString("en-US", options); 
        timeList.push(dateFormatted); //Uses local date of the user and converts it into US format
    };
    timeList.reverse(); //to display the most recent time period first
    for(var i = 0; i < timeList.length; i++) {
        var opt = timeList[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    };
};