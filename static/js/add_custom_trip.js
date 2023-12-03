$(document).ready(function () {
    // DISPLAY MAP
    // initialize Leaflet
    var map = L.map('map').setView({
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

    // ADD LOCATIONS

    const provider = new GeoSearch.OpenStreetMapProvider();

    const search = new GeoSearch.GeoSearchControl({
        provider: new GeoSearch.OpenStreetMapProvider(),
        style: "bar",
        autoClose: true,
    });
    // on add location button click open map search
    $("#add-location").click(function (e) {
        e.preventDefault();

        map.addControl(search);
    });

    // search result event handler, create a new li in form storing name and coordinates
    function searchEventHandler(result) {
        // TESTING
        console.log(result.location);

        let locationName = result.location.label;

        $("#locations-list").append(
            `<li>
                <input type="text" value=${locationName}>
                <input type="number" name="lat" value=${result.location.x} hidden>
                <input type="number" name="long" value=${result.location.y} hidden>
            </li>`
        );

        map.removeControl(search);
    }

    // trigger search result even handler
    map.on('geosearch/showlocation', searchEventHandler);
});