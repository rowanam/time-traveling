$(document).ready(function () {
    /**
     * Set map height - aspect ratio 3:2, based on width
     */
    function setMapHeight() {
        $("#map").height($("#map").width() * 2 / 3);
    }

    // set map height on page load and window resize
    setMapHeight();
    $(window).resize(setMapHeight);

    // RENDER MAP
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

    // create a red polyline from the array of LatLng points
    var polyline = L.polyline(coordinates, {
        color: 'orange',
        weight: 2,
    }).addTo(map);

    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
});