// initialise the map and set coordinates on Birmingham, zoomed out to show UK
var map = L.map('map').setView([52.4862, -1.8904], 7);

// Add map tiles and attribution
L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18
}).addTo(map);

// An array of the location of the GPX files

var gpxs = [
  '/assets/LEJoG_day_one.gpx',
  '/assets/LEJoG_day_two.gpx',
  '/assets/LEJoG_day_three.gpx',
  '/assets/LEJoG_day_four.gpx',
  '/assets/LEJoG_day_five.gpx',
  '/assets/LEJoG_day_six.gpx',
  '/assets/LEJoG_day_seven.gpx',
  '/assets/LEJoG_day_eight.gpx',
  '/assets/LEJoG_day_nine.gpx',
  '/assets/LEJoG_day_ten.gpx',
  '/assets/LEJoG_day_eleven.gpx',
  '/assets/LEJoG_day_twelve.gpx',
  '/assets/LEJoG_day_thirteen.gpx',
  '/assets/LEJoG_day_fourteen.gpx',
  '/assets/LEJoG_day_fifteen.gpx',
  '/assets/LEJoG_day_sixteen.gpx'
];

// Iterate through the array and put the routes on the map, calling the icons for start and finish points

for (var i = 0; i < gpxs.length; i++) {
  gpx = gpxs[i];

  new L.GPX(gpx, {
    async: true,
    marker_options: {
        startIconUrl: 'pin-icon-start.png',
        endIconUrl: 'pin-icon-end.png',
        shadowUrl: 'pin-shadow.png'
      }
  }).on('loaded', function(i) { return function(e) {
      if (gpxs.length - 1 === i) {
        map.fitBounds(e.target.getBounds());
      }
    };
  }(i)).addTo(map);
}