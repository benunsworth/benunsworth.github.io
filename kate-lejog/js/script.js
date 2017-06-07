// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([51.4876, -0.2672], 9);

// Add map tiles and attribution
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);

// no idea how to just iterate through the assets... so adding one by one

var gpx = '/assets/LEJoG_day_one.gpx'; // URL to your GPX file
new L.GPX(gpx, {
	async: true,
	marker_options: {
    	startIconUrl: 'pin-icon-start.png',
    	endIconUrl: 'pin-icon-end.png',
    	shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx2 = '/assets/pLEJoG_day_two.gpx'; // URL to your GPX file
new L.GPX(gpx2, {
	async: true,
	marker_options: {
    	startIconUrl: 'pin-icon-start.png',
    	endIconUrl: 'pin-icon-end.png',
    	shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx3 = '/assets/pLEJoG_day_three.gpx'; // URL to your GPX file
new L.GPX(gpx3, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx4 = '/assets/pLEJoG_day_four.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx4, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx5 = '/assets/pLEJoG_day_five.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx5, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);