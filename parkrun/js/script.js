// initialise the map and set coordinates centred on Chiswick to catch all my London parkruns
var map = L.map('map').setView([51.4876, -0.2672], 9);

// Add map tiles and attribution
  L.tileLayer('http://{s}.tiles.mapbox.com/v3/benunsworth.k7ao6p15/{z}/{x}/{y}.png', {
    	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    	maxZoom: 18
	}).addTo(map);

// add markers and popups to the map
L.marker([51.410992, -0.335791]).addTo(map).bindPopup("<b>Bushy Park</b><br>PB: 17:46<br>Runs: 28");
L.marker([51.451962, -0.292886]).addTo(map).bindPopup("<b>Richmond Park</b><br>PB: 19:25<br>Runs: 24");
L.marker([51.440762, -0.451523]).addTo(map).bindPopup("<b>Bedfont Lakes</b><br>PB: 17:51<br>Runs: 3");
L.marker([51.455132, 0.113254]).addTo(map).bindPopup("<b>Bexley</b><br>PB: 24:34<br>Runs: 1");
L.marker([51.433342, -0.146770]).addTo(map).bindPopup("<b>Tooting Common</b><br>PB: 19:25<br>Runs: 5");
L.marker([51.472465, -0.218493]).addTo(map).bindPopup("<b>Fulham Palace</b><br>PB: 19:07<br>Runs: 1");
L.marker([51.443869, -0.079206]).addTo(map).bindPopup("<b>Dulwich</b><br>PB: 19:37<br>Runs: 16");
L.marker([50.971433, -1.374032]).addTo(map).bindPopup("<b>Eastleigh</b><br>PB: 23:40<br>Runs: 1");
L.marker([51.484536, -0.081024]).addTo(map).bindPopup("<b>Burgess</b><br>PB: 19:40<br>Runs: 3");
L.marker([50.792835, -3.455007]).addTo(map).bindPopup("<b>Killerton</b><br>PB: 20:54<br>Runs: 1");
L.marker([51.452538, -0.105464]).addTo(map).bindPopup("<b>Brockwell</b><br>PB: 19:49<br>Runs: 8");
L.marker([51.455486, -0.060688]).addTo(map).bindPopup("<b>Peckham Rye</b><br>PB: 19:16<br>Runs: 2");
L.marker([51.460143, -0.025019]).addTo(map).bindPopup("<b>Hilly Fields</b><br>PB: 20:07<br>Runs: 1");
L.marker([51.419846, -0.065703]).addTo(map).bindPopup("<b>Crystal Palace</b><br>PB: 19:48<br>Runs: 5");
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
L.marker([51.386539, 0.022874]).addTo(map).bindPopup("<b>Bromley</b><br>PB: 20:40<br>Runs: 3");
L.marker([51.138190, -0.491510]).addTo(map).bindPopup("<b>Cranleigh</b><br>PB: 23:38<br>Runs: 1");
L.marker([51.265798, -0.755847]).addTo(map).bindPopup("<b>Rushmoor</b><br>PB: 21:05<br>Runs: 1");
L.marker([51.311708, -0.556204]).addTo(map).bindPopup("<b>Woking</b><br>PB: 26:34<br>Runs: 1");
L.marker([51.449459, 0.075155]).addTo(map).bindPopup("<b>Greenwich</b><br>PB: 21:37<br>Runs: 1");
L.marker([51.540329, -0.547600]).addTo(map).bindPopup("<b>Black Park</b><br>PB: 20:57<br>Runs: 1");
L.marker([51.558598, -0.168185]).addTo(map).bindPopup("<b>Hampstead Heath</b><br>PB: 23:38<br>Runs: 1");
L.marker([51.366808, -0.539078]).addTo(map).bindPopup("<b>Homewood</b><br>PB: 22:59<br>Runs: 1");
L.marker([51.417952, -0.006042]).addTo(map).bindPopup("<b>Beckenham Place</b><br>PB: 20:00<br>Runs: 1");
L.marker([51.168607, -0.838140]).addTo(map).bindPopup("<b>Alice Holt</b><br>PB: 22:42<br>Runs: 1");
L.marker([51.396111, -0.059908]).addTo(map).bindPopup("<b>South Norwood</b><br>PB: 20:44<br>Runs: 9");
L.marker([51.365283, 0.117224]).addTo(map).bindPopup("<b>Orpington</b><br>PB: 22:44<br>Runs: 1");
L.marker([51.318485, -0.079549]).addTo(map).bindPopup("<b>Riddlesdown</b><br>PB: 27:33<br>Runs: 1");
L.marker([51.298622, -0.724851]).addTo(map).bindPopup("<b>Frimley Lodge</b><br>PB: 22:50<br>Runs: 1");
L.marker([51.234350, -0.208644]).addTo(map).bindPopup("<b>Reigate Priory</b><br>PB: 30:35<br>Runs: 1");
L.marker([51.097000, -0.175623]).addTo(map).bindPopup("<b>Tilgate</b><br>PB: 30:38<br>Runs: 1");
L.marker([50.810312, -0.364500]).addTo(map).bindPopup("<b>Worthing</b><br>PB: 20:56<br>Runs: 1");
L.marker([51.786634, -0.659599]).addTo(map).bindPopup("<b>Tring</b><br>PB: 25:40<br>Runs: 1");
L.marker([51.353118, 0.187147]).addTo(map).bindPopup("<b>Lullingstone</b><br>PB: 26.43<br>Runs: 1");
L.marker([51.307648, -0.184225]).addTo(map).bindPopup("<b>Banstead Woods</b><br>PB: 26:26<br>Runs: 1");
L.marker([51.685080, -4.206204]).addTo(map).bindPopup("<b>Llanelli Coast</b><br>PB: 19:23<br>Runs: 1");
L.marker([51.448240, -0.008630]).addTo(map).bindPopup("<b>Catford</b><br>PB: 22:32<br>Runs: 1");
L.marker([52.935408, -1.504769]).addTo(map).bindPopup("<b>Markeaton</b><br>PB: 19:16<br>Runs: 1");
L.marker([51.455873, -0.151331]).addTo(map).bindPopup("<b>Clapham Common</b><br>PB: 20:43<br>Runs: 1");
L.marker([51.831620, -0.838394]).addTo(map).bindPopup("<b>Aylesbury</b><br>PB: 21:08 <br>Runs: 3");
L.marker([52.050110, -0.722984]).addTo(map).bindPopup("<b>Milton Keynes</b><br>PB: 23:11<br>Runs: 1"),
L.marker([52.058640, -0.760168]).addTo(map).bindPopup("<b>Linford Wood</b><br>PB: 22:29<br>Runs: 1"),
L.marker([51.947057, -0.674095]).addTo(map).bindPopup("<b>Rushmere</b><br>PB: 31:25<br>Runs: 1"),
L.marker([51.901550, -0.510046]).addTo(map).bindPopup("<b>Houghton Hall</b><br>PB: 25:52<br>Runs: 1"),
L.marker([52.262374, -1.157320]).addTo(map).bindPopup("<b>Daventry</b><br>PB: 23:22<br>Runs: 1");
L.marker([51.541272, -0.376711]).addTo(map).bindPopup("<b>Northala Fields</b><br>PB: 21:51<br>Runs: 1")
// for new rows L.marker([]).addTo(map).bindPopup("<b>event name</b><br>PB: <br>Runs: 1")


