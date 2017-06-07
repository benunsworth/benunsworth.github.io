// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([51.4876, -0.2672], 9);

// Add map tiles and attribution
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);

var gpx = '/assets/Long_slow_run.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx, {async: true}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);