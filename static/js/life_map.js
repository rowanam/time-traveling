$(document).ready(function () {
    // initialize Leaflet
    const map = L.map('map').setView({
        lon: 0,
        lat: 0
    }, 2);

    // add CartoDB_Voyager map tiles
    const CartoDB_Voyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    });
    CartoDB_Voyager.addTo(map);

    // store Esri_WorldImagery tiles
    const Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });

    let currentStyle = 0;

    // switch between tile providers on button click
    $("#life-map-style-toggle").click(function () {
        if (currentStyle == 0) {
            CartoDB_Voyager.remove();
            Esri_WorldImagery.addTo(map);
            currentStyle = 1;
        } else {
            Esri_WorldImagery.remove();
            CartoDB_Voyager.addTo(map);
            currentStyle = 0;
        }
    });

    // show the scale bar on the lower left corner
    L.control.scale({
        imperial: true,
        metric: true
    }).addTo(map);

    let coordinates = JSON.parse(document.getElementById('coordinates').textContent);

    // create a polyline from the array of coordinates
    let polyline = L.polyline(coordinates, {
        color: 'orange',
        weight: 1,
    }).addTo(map);
});