// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([52.4862, 1.8904°], 3);

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

var gpx2 = '/assets/LEJoG_day_two.gpx'; // URL to your GPX file
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

var gpx3 = '/assets/LEJoG_day_three.gpx'; // URL to your GPX file
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

var gpx4 = '/assets/LEJoG_day_four.gpx'; // URL to your GPX file or the GPX itself
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

var gpx5 = '/assets/LEJoG_day_five.gpx'; // URL to your GPX file or the GPX itself
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

var gpx6 = '/assets/LEJoG_day_six.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx6, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx7 = '/assets/LEJoG_day_seven.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx7, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx8 = '/assets/LEJoG_day_eight.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx8, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx9 = '/assets/LEJoG_day_nine.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx9, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx10 = '/assets/LEJoG_day_ten.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx10, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx11 = '/assets/LEJoG_day_eleven.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx11, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx12 = '/assets/LEJoG_day_twelve.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx12, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx13 = '/assets/LEJoG_day_thirteen.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx13, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);

var gpx14 = '/assets/LEJoG_day_fourteen.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx14, {
  async: true,
  marker_options: {
      startIconUrl: 'pin-icon-start.png',
      endIconUrl: 'pin-icon-end.png',
      shadowUrl: 'pin-shadow.png'
    }
}).on('loaded', function(e) {
  map.fitBounds(e.target.getBounds());
}).addTo(map);