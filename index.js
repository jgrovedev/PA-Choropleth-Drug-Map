//SETS STYLE TO TOTAL GEOJSON DATA
var total_layer = L.geoJson(totalData) 
    function getColor_blue(d) { //sets choropleth colors colorbrewer2.org
        return d > 489  ? '#084594' :
            d > 408  ? '#2171b5' :
            d > 326  ? '#4292c6' :
            d > 245  ? '#6baed6' :
            d > 163  ? '#9ecae1' :
            d > 82   ? '#c6dbef' :
                        '#eff3ff';
    }
    function style_total(feature) { //applies color to selected geoJSON property
        return {
            fillColor: getColor_blue(feature.properties.rate),
            weight: 1,
            opacity: 1,
            color: 'black',
            fillOpacity: 0.7
        };
    }
;

//SETS STYLE TO HERION GEOJSON DATA
var her_layer = L.geoJson(herData) 
    function getColor_red(d) { //sets choropleth colors colorbrewer2.org
        return d > 472  ? '#99000d' :
            d > 394  ? '#cb181d' :
            d > 315  ? '#ef3b2c' :
            d > 236  ? '#fb6a4a' :
            d > 157  ? '#fc9272' :
            d > 79   ? '#fcbba1' :
                        '#fee5d9';
    }
    function style_her(feature) { //applies color to selected geoJSON property
        return {
            fillColor: getColor_red(feature.properties.rate),
            weight: 1,
            opacity: 1,
            color: 'black',
            fillOpacity: 0.7
        };
    }
;

//SETS STYLE TO FENTANYL GEOJSON DATA
var fen_layer = L.geoJson(fenData) 
    function getColor_green(d) { //sets choropleth colors colorbrewer2.org
        return d > 18  ? '#005824' :
            d > 15  ? '#238b45' :
            d > 12  ? '#41ae76' :
            d > 9  ? '#66c2a4' :
            d > 6  ? '#99d8c9' :
            d > 3   ? '#ccece6' :
                        '#edf8fb';
    }
    function style_fen(feature) { //applies color to selected geoJSON property
        return {
            fillColor: getColor_green(feature.properties.rate),
            weight: 1,
            opacity: 1,
            color: 'black',
            fillOpacity: 0.7,
        };
    }
;

var opi_layer = L.geoJson(opiData)
    function getColor_purple(d) { //sets choropleth colors colorbrewer2.org
        return d > 24  ? '#4a1486' :
            d > 20  ? '#6a51a3' :
            d > 16  ? '#807dba' :
            d > 12  ? '#9e9ac8' :
            d > 8  ? '#bcbddc' :
            d > 4   ? '#dadaeb' :
                        '#f2f0f7';
    }
    function style_opi(feature) { //applies color to selected geoJSON property
        return {
            fillColor: getColor_purple(feature.properties.rate),
            weight: 1,
            opacity: 1,
            color: 'black',
            fillOpacity: 0.7,
        };
    }
;

//SETS MAP STARTING LOCATION
var map = L.map('map',{
    center: [41.05, -77.5],
    zoom: 8,
    minZoom: 2,
    maxZoom: 18,
    layers: [total_layer],
});

//CREATES TILE LAYER
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: ""
}).addTo(map);

// CREATES CONTROL LAYERS TO SWITCH BETWEEN MAPS
var baseMaps = {
    "Total": total_layer,
    "Herion": her_layer,
    "Fentanyl": fen_layer,
    "Opium": opi_layer,
};

L.control.layers(baseMaps).addTo(map);

//************CUSTOM INFO CONTROL************

//ROUNDS DATA IN INFO CONTROL
function round(value, decimals) {
    return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
  }

//CREATES A DIV ON MAP TO DISPLAY GEOJSON INFO
var info = L.control({position: 'topright'});

info.onAdd = function(map) {
    this._div = L.DomUtil.create('div', 'info'); // creates a div with a class "info"
    this.update();
    return this._div;
};

//FILLS CREATED DIV WITH GEOJSON INFO
info.update = function (properties) {
    this._div.innerHTML = '<h4>County Information</h4>' + (properties ?
        '<b>' + "Name: " + '</b>' + properties.county_name + '<br>'
      + '<b>' + "Arrests: " + '</b>' + properties.arrests + '<br>'
      + '<b>' + "Incident Count: " + '</b>' + properties.incident_count + '<br>'
      + '<b>' + "Incident Total: " + '</b>' + properties.incident_total + '<br>'
      + '<b>' + "Drug Quanity (kg): " + '</b>' + round(properties.drug_quantity, 2) + '<br>'
      + '<b>' + "Population: " + '</b>' + properties.population + '<br>'
      + '<b>' + "Incident Rate: " + '</b>' + round(properties.rate, 2) + '<br>'
      + "" : 'Hover over county')
    };

info.addTo(map);

//APPLYS HIGHLIGHT FEATURE
function highlightFeature(e) {
    var layer = e.target;

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

//APPLYS CLICK ZOOOM FEATURE WHEN TARGET IS CLICKED
function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

//APPLYS FUNCTIONS ON EACH FEATURE USING MOUSEOVER AND CLICK
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        click: zoomToFeature
    });
}

//STYLES DATA FROM GEOJSON AND APPLIES THE LAYER TO MAP
L.geoJson(totalData, {
    style: style_total,
    onEachFeature: onEachFeature
    }).addTo(total_layer);

L.geoJson(herData, {
    style: style_her,
    onEachFeature: onEachFeature
    }).addTo(her_layer);

L.geoJson(fenData, {
    style: style_fen,
    onEachFeature: onEachFeature
    }).addTo(fen_layer);

L.geoJson(opiData, {
    style: style_opi,
    onEachFeature: onEachFeature
    }).addTo(opi_layer);

//************CREATES LEGENDS************

var total_legend = L.control({position: 'bottomright'});
var her_legend = L.control({position: 'bottomright'});
var fen_legend = L.control({position: 'bottomright'});
var opi_legend = L.control({position: 'bottomright'});

total_legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'), // creates a div with a class "info legend"
        grades = [0, 82, 163, 245, 326, 408, 489],
        labels = [];
    div.innerHTML = '<h4>' + 'Incident Rate' + '<h4>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_blue(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

her_legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'), // creates a div with a class "info legend"
        grades = [0, 79, 157, 236, 315, 494, 472],
        labels = [];
    div.innerHTML = '<h4>' + 'Incident Rate' + '<h4>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_red(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

fen_legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'), // creates a div with a class "info legend"
        grades = [0, 3, 6, 9, 12, 15, 18],
        labels = [];
    div.innerHTML = '<h4>' + 'Incident Rate' + '<h4>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_green(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

opi_legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'), // creates a div with a class "info legend"
        grades = [0, 4, 8, 12, 16, 20, 24],
        labels = [];
    div.innerHTML = '<h4>' + 'Incident Rate' + '<h4>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_purple(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

total_legend.addTo(map);
map.on('baselayerchange', function (eventLayer) {
    if (eventLayer.name === 'Total') {
        map.removeControl(her_legend);
        map.removeControl(fen_legend);
        map.removeControl(opi_legend);
        total_legend.addTo(map);
    } else if (eventLayer.name === 'Herion') {
        map.removeControl(total_legend);
        map.removeControl(fen_legend);
        map.removeControl(opi_legend);
        her_legend.addTo(map);
    } else if (eventLayer.name === 'Fentanyl') {
        map.removeControl(her_legend);
        map.removeControl(total_legend);
        map.removeControl(opi_legend);
        fen_legend.addTo(map);
    } else if (eventLayer.name === 'Opium') {
        map.removeControl(fen_legend);
        map.removeControl(total_legend);
        map.removeControl(her_legend);
        opi_legend.addTo(map);
    }
});