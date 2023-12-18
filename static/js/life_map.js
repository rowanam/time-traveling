$(document).ready(function () {
    // initialize Leaflet
    const map = L.map('map').setView({
        lon: 0,
        lat: 0
    }, 2);

    // add the OpenStreetMap tiles
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

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
})