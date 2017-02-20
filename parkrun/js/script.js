// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([51.4876, -0.2672], 9);

// Add map tiles and attribution
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);

// add markers and popups to the map
L.marker([51.410992, -0.335791]).addTo(map).bindPopup("<b>Bushy Park</b><br>PB: 17:46<br>Runs: 28");
L.marker([51.451962, -0.292886]).addTo(map).bindPopup("<b>Richmond Park</b><br>PB: 19:25<br>Runs: 20");
L.marker([51.440762, -0.451523]).addTo(map).bindPopup("<b>Bedfont Lakes</b><br>PB: 17:51<br>Runs: 3");
L.marker([51.433342, -0.146770]).addTo(map).bindPopup("<b>Tooting Common</b><br>PB: 19:25<br>Runs: 4");
L.marker([51.472465, -0.218493]).addTo(map).bindPopup("<b>Fulham Palace</b><br>PB: 19:07<br>Runs: 1");
L.marker([51.443869, -0.079206]).addTo(map).bindPopup("<b>Dulwich</b><br>PB: 19:37<br>Runs: 2");
L.marker([50.971433, -1.374032]).addTo(map).bindPopup("<b>Eastleigh</b><br>PB: 23:40<br>Runs: 1");
L.marker([51.484536, -0.081024]).addTo(map).bindPopup("<b>Burgess</b><br>PB: 19:40<br>Runs: 1");
L.marker([50.792835, -3.455007]).addTo(map).bindPopup("<b>Killerton</b><br>PB: 20:54<br>Runs: 1");
L.marker([51.452538, -0.105464]).addTo(map).bindPopup("<b>Brockwell</b><br>PB: 19:49<br>Runs: 2");
L.marker([51.455486, -0.060688]).addTo(map).bindPopup("<b>Peckham Rye</b><br>PB: 19:16<br>Runs: 1");
L.marker([51.460143, -0.025019]).addTo(map).bindPopup("<b>Hilly Fields</b><br>PB: 20:07<br>Runs: 1");
L.marker([51.419846, -0.065703]).addTo(map).bindPopup("<b>Crystal Palace</b><br>PB: 19:48<br>Runs: 2");
L.marker([55.978806, -3.291585]).addTo(map).bindPopup("<b>Edinburgh</b><br>PB: 23:58<br>Runs: 1");
L.marker([51.356926, -0.231078]).addTo(map).bindPopup("<b>Nonsuch</b><br>PB: 21:17<br>Runs: 1");
L.marker([51.520412, -0.238523]).addTo(map).bindPopup("<b>Wormwood Scrubs</b><br>PB: 24:07<br>Runs: 1");
L.marker([51.426567, -0.309516]).addTo(map).bindPopup("<b>Kingston</b><br>PB: 19:33<br>Runs: 1");
L.marker([51.442078, -0.232215]).addTo(map).bindPopup("<b>Wimbledon Common</b><br>PB: 19:54<br>Runs: 1");
L.marker([51.441168, -0.372075]).addTo(map).bindPopup("<b>Crane Park</b><br>PB: 22:01<br>Runs: 1");
L.marker([51.365295, 1.041942]).addTo(map).bindPopup("<b>Whitstable</b><br>PB: 20:04<br>Runs: 1");
L.marker([51.247383, -0.562062]).addTo(map).bindPopup("<b>Guildford</b><br>PB: 22:13<br>Runs: 1");
L.marker([51.364807, -0.079973]).addTo(map).bindPopup("<b>Lloyd</b><br>PB: 21:56<br>Runs: 2");
L.marker([51.489403, -0.349889]).addTo(map).bindPopup("<b>Osterley</b><br>PB: 21:37<br>Runs: 1");
L.marker([51.352253, -0.118720]).addTo(map).bindPopup("<b>Roundshaw Downs</b><br>PB: 26:07<br>Runs: 1");
L.marker([51.464417, -0.306973]).addTo(map).bindPopup("<b>Old Deer Park</b><br>PB: 22:39<br>Runs: 1");
L.marker([51.499405, -0.292253]).addTo(map).bindPopup("<b>Gunnersbury</b><br>PB: 21:17<br>Runs: 1");
L.marker([51.386539, 0.022874]).addTo(map).bindPopup("<b>Bromley</b><br>PB: 20:40<br>Runs: 1");
L.marker([51.138190, -0.491510]).addTo(map).bindPopup("<b>Cranleigh</b><br>PB: 23:38<br>Runs: 1");
L.marker([51.265798, -0.755847]).addTo(map).bindPopup("<b>Rushmoor</b><br>PB: 21:05<br>Runs: 1");
L.marker([51.311708, -0.556204]).addTo(map).bindPopup("<b>Woking</b><br>PB: 26:34<br>Runs: 1");
L.marker([51.449459, 0.075155]).addTo(map).bindPopup("<b>Greenwich</b><br>PB: 21:37<br>Runs: 1");
L.marker([51.540329, -0.547600]).addTo(map).bindPopup("<b>Black Park</b><br>PB: 20:57<br>Runs: 1");
L.marker([51.558598, -0.168185]).addTo(map).bindPopup("<b>Hampstead Heath</b><br>PB: 23:38<br>Runs: 1");
L.marker([51.366808, -0.539078]).addTo(map).bindPopup("<b>Homewood</b><br>PB: 22:59<br>Runs: 1")