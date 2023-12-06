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

    // INITIALIZE MAP SEARCH
    const provider = new GeoSearch.OpenStreetMapProvider();

    const search = new GeoSearch.GeoSearchControl({
        provider: new GeoSearch.OpenStreetMapProvider(),
        style: "bar",
        autoClose: true,
    });

    // ADD LOCATIONS
    // on add location button click, open map search
    $("#add-location").click(function (e) {
        e.preventDefault();

        map.addControl(search);
    });

    // add a new form to page with data from the search result
    function searchEventHandler(result) {
        // get current total number of forms, which will be the next form index
        let formIndex = $("#id_form-TOTAL_FORMS").val();

        // add a new form - html content of empty-form with correct index added to id and name attributes
        $("#locations-list").append($("#empty-form").html().replace(/__prefix__/g, formIndex));
        
        // get results from map search and store location name and coordinate data
        let locationName = result.location.label;
        let lat = result.location.x;
        let long = result.location.y;

        // add location data and list order to newly created form
        $(`#id_form-${formIndex}-name`).val(locationName);
        $(`#id_form-${formIndex}-lat`).val(lat);
        $(`#id_form-${formIndex}-long`).val(long);
        $(`#id_form-${formIndex}-order`).val(parseInt(formIndex) + 1);

        // increment total forms in management form
        $("#id_form-TOTAL_FORMS").val(parseInt(formIndex) + 1);

        // remove search bar from map
        map.removeControl(search);
    }

    // when user selects a location from map search, trigger search result even handler
    map.on('geosearch/showlocation', searchEventHandler);
});