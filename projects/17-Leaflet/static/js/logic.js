// Store our API endpoint as queryUrl
    var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson";
// var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

var tectonicPlatesGeoJson = "data/tectonicplates-master/GeoJSON/PB2002_plates.json";

//Perform a GET request to the query URL
var quakes = d3.json(queryUrl, function(data) {
    // Once we get a response, send the data.features object to the createFeatures function
    eqFeatures(data.features);
});

function getColor(mag){
    var color;
    if(mag <=1){
        color = "#fef0d9"; //beige
    }
    else if(mag <=2){
        color = "#fdd49e"; //light peach
    }
    else if (mag <=3){
        color = "#fdbb84"; //peach
    }
    else if (mag <=4){
        color = "#fc8d59"; //salmon
    }
    else if (mag <=5){
        color = "#e34a33"; //orange
    }
    else{
        color = "#b30000"; //red
    }
    return color;
}

// Selects different opacity for the circle depending on magnitude of earthquake
function getOpacity(mag){
    var opacity;
    if(mag <=1){
        opacity = 0.1;
    }
    else if(mag <=2){
        opacity = 0.3;
    }
    else if (mag <=3){
        opacity = 0.5; 
    }
    else if (mag <=4){
        opacity = 0.7; 
    }
    else if (mag <=5){
        opacity = 0.9; 
    }
    else{
        opacity = 1; 
    }
    return opacity;
}

function plateFeatures(earthquakes, plateData){
    // Create a GeoJSON layer containing the features array on the tectonic plate object
    // Run the onEachFeature function once for each piece of data in the array
    function onEachFeature(feature,layer){
        layer.bindPopup("<h3>"+feature.properties.PlateName + "</h3>");
    }
    
    var plates = L.geoJSON(plateData, {
        onEachFeature: onEachFeature, 
        pointToLayer: function(feature, latlng){
            return L.circleMarker(latlng, {
                color: "black",
                opacity: 0.3,
                weight: 1,
                opacity: 1,
            })
        }
    });

    // Sending our earthquakes and plates layer to the createMap function
    createMap(earthquakes, plates);
}

function eqFeatures(earthquakeData) {
    // Define a function we want to run once for each feature in the features array
    // Give each feature a popup describing the place and time of the earthquake
    function onEachFeature(feature, layer) {
        layer.bindPopup("<h3>Location: " + feature.properties.place +
        "</h3><hr><p>Date: " + new Date(feature.properties.time) + 
        "<br>Magnitude: "+ feature.properties.mag + "</p>");
    }

    // Create a GeoJSON layer containing the features array on the earthquakeData object
    // Run the onEachFeature function once for each piece of data in the array
    var earthquakes = L.geoJSON(earthquakeData, {
        onEachFeature: onEachFeature, 
        pointToLayer: function(feature, latlng){
            return L.circleMarker(latlng, {
                radius: (feature.properties.mag*4),
                color: "black",
                opacity: 0.3,
                fillColor: getColor(feature.properties.mag),
                weight: 1,
                opacity: 1,
                fillOpacity: getOpacity(feature.properties.mag)
            })
        }
    });

    // Sending our earthquakes layer along with Tectonic Plates GeoJSON to the plateFeatures function
    d3.json(tectonicPlatesGeoJson, function(data){
        plateFeatures(earthquakes, data.features);
    });
}
  
function createMap(earthquakes, plates) {
  
    // Define streetmap and darkmap layers
    var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.streets",
      accessToken: API_KEY
    });

    var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.dark",
        accessToken: API_KEY
    });
  
    var satellitemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.satellite",
        accessToken: API_KEY
    });

    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Street Map": streetmap, 
      "Dark Map": darkmap, 
      "Satellite Map": satellitemap
    };
  
    // Create overlay object to hold our overlay layer
    var overlayMaps = {
      "Earthquakes": earthquakes,
      "Plates": plates
    };
  
    // Create our map, giving it the streetmap, tectonic plates, and earthquakes layers to display on load
    var myMap = L.map("map", {
      center: [
        37.09, -95.71
      ],
      zoom: 4,
      layers: [streetmap, plates, earthquakes]
    });
  
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap);

    // Creating legend for earthquake magnitude colors
    var legend = L.control({position: 'bottomright'});
        legend.onAdd = function(myMap){
            var div = L.DomUtil.create('div', 'info legend'),
                quakeScale = [0,1,2,3,4,5], 
                labels = [];

            for (var i=0; i<quakeScale.length; i++){
                div.innerHTML +=
                    '<i style="background:' + getColor(quakeScale[i]+1) + '"></i> ' + 
                    quakeScale[i] + (quakeScale[i+1] ? '&ndash;' + quakeScale[i+1] + '<br>' : '+');
            }
            return div;
        };
    legend.addTo(myMap);
}
  