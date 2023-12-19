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

    // add CartoDB_Voyager map tiles
    const CartoDB_Voyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    });
    CartoDB_Voyager.addTo(map);

    // show the scale bar on the lower left corner
    L.control.scale({
        imperial: true,
        metric: true
    }).addTo(map);

    let coordinates = JSON.parse(document.getElementById('coordinates').textContent);

    // create a polyline from the array of coordinates
    if (coordinates.length >= 2) {
        let polyline = L.polyline(coordinates, {
            color: 'orange',
            weight: 2,
        }).addTo(map);

        // zoom the map to the polyline
        map.fitBounds(polyline.getBounds());
    }
});