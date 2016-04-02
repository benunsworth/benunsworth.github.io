// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([51.4876, -0.2672], 11);

// Add map tiles and attribution
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);

// add markers and popups to the map
L.marker([51.410992, -0.335791]).addTo(map).bindPopup("<b>Bushy Park</b><br>PB: 17:46<br>Runs: 28");
L.marker([51.451962, -0.292886]).addTo(map).bindPopup("<b>Richmond Park</b><br>PB: 19:25<br>Runs: 17");
L.marker([51.440762, -0.451523]).addTo(map).bindPopup("<b>Bedfont Lakes</b><br>PB: 17:51<br>Runs: 3");
L.marker([51.433342, -0.146770]).addTo(map).bindPopup("<b>Tooting Common</b><br>PB: 19:25<br>Runs: 3");
L.marker([51.472465, -0.218493]).addTo(map).bindPopup("<b>Fulham Palace</b><br>PB: 19:07<br>Runs: 1");
L.marker([51.443869, -0.079206]).addTo(map).bindPopup("<b>Dulwich</b><br>PB: 19:37<br>Runs: 1");
L.marker([50.971433, -1.374032]).addTo(map).bindPopup("<b>Eastleigh</b><br>PB: 23:40<br>Runs: 1");
L.marker([51.484536, -0.081024]).addTo(map).bindPopup("<b>Burgess</b><br>PB: 19:40<br>Runs: 1");
L.marker([50.792835, -3.455007]).addTo(map).bindPopup("<b>Killerton</b><br>PB: 20:54<br>Runs: 1");
L.marker([51.452538, -0.105464]).addTo(map).bindPopup("<b>Brockwell</b><br>PB: 19:49<br>Runs: 1");
L.marker([51.455486, -0.060688]).addTo(map).bindPopup("<b>Peckham Rye</b><br>PB: 19:16<br>Runs: 1");
L.marker([51.460143, -0.025019]).addTo(map).bindPopup("<b>Hilly Fields</b><br>PB: 20:07<br>Runs: 1");
L.marker([51.419846, -0.065703]).addTo(map).bindPopup("<b>Crystal Palace</b><br>PB: 19:48<br>Runs: 1");
L.marker([55.978806, -3.291585]).addTo(map).bindPopup("<b>Edinburgh</b><br>PB: 23:58<br>Runs: 1");
