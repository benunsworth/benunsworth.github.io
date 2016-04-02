
// Use jQuery's getJSON() to make API Call to Bath: Hacked Datastore, filter for location and notes columns only
  $.getJSON('http://data.bathhacked.org/resource/2pme-edif.json?$select=location,%20name,%20closingtime', function(results) {
  console.log(results.data);
  var map = L.map('map').setView([51.380888, -2.361460], 15);
      
// Add map tiles from mapbox, include relevant attributions and set zoom level
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);
      
// Replace standard leaflet popup with a pint icon
var pubIcon = L.icon({
	iconUrl: 'http://www.fancyapint.com/images/icon_traditional_inn.png',
	iconSize: 		[32, 37], // set icon size
	iconAnchor: 	[16, 37], // set icon anchor point
	popupAnchor: 	[1, -37]  // point from which the popup opens relative to the icon anchor
});
      
// Iterate through API data and place markers on the map, with information from notes column in datastore
	results.forEach(function(result){
		console.log(result);
		L.marker([result.location.latitude, result.location.longitude], {icon: pubIcon})
			.bindPopup(
				'<h4>' + result.name + '<h4>'
			)
			.addTo(map);
	})
});