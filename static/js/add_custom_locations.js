import { setMapHeight } from './map_sizing.js';

$(document).ready(function () {
    // size map on page load and window resizing
    setMapHeight();
    $(window).resize(setMapHeight);
    
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

    // INITIALIZE CURRENT LOCATION RESULT VARIABLE
    let currentLocationObject = null;

    // ADD AUTOCOMPLETE SEARCH BAR
    const auto = new Autocomplete("search", {
        // default selects the first item in
        // the list of results
        selectFirst: true,

        // The number of characters entered should start searching
        howManyCharacters: 2,

        // onSearch
        onSearch: ({
            currentValue
        }) => {
            const api = `https://nominatim.openstreetmap.org/search?format=geojson&limit=5&city=${encodeURI(
            currentValue
        )}`;

            /**
             * Promise
             */
            return new Promise((resolve) => {
                fetch(api)
                    .then((response) => response.json())
                    .then((data) => {
                        resolve(data.features);
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            });
        },
        // nominatim GeoJSON format parse - this part turns json into the list of
        // records that appears when you type.
        onResults: ({
            currentValue,
            matches,
            template
        }) => {
            const regex = new RegExp(currentValue, "gi");

            // if the result returns 0 we
            // show the no results element
            return matches === 0 ?
                template :
                matches
                .map((element) => {
                    return `
            <li class="loupe">
              <p>
                ${element.properties.display_name.replace(
                  regex,
                  (str) => `<b>${str}</b>`
                )}
              </p>
            </li> `;
                })
                .join("");
        },

        // on selection of a result
        onSubmit: ({
            object
        }) => {
            // remove all layers from the map
            map.eachLayer(function (layer) {
                if (!!layer.toGeoJSON) {
                    map.removeLayer(layer);
                }
            });

            // display result on map
            const {
                display_name
            } = object.properties;
            const [lng, lat] = object.geometry.coordinates;

            const marker = L.marker([lat, lng], {
                title: display_name,
            });

            marker.addTo(map).bindPopup(display_name);

            map.setView([lat, lng], 8);

            // display "Add" button
            $("#add-location").show();

            // store current location result
            currentLocationObject = object;
        },

        // the method presents no results element
        noResults: ({
                currentValue,
                template
            }) =>
            template(`<li>No results found: "${currentValue}"</li>`),
    });

    // add a new form to page with data from the search result
    function addLocationForm(resultObject) {
        // get current total number of forms, which will be the next form index
        let formIndex = $("#id_form-TOTAL_FORMS").val();

        // add a new form - html content of empty-form with correct index added to id and name attributes
        $("#locations-list").append($("#empty-form").html().replace(/__prefix__/g, formIndex));

        // get results from map search and store location name and coordinate data
        let locationName = resultObject.properties.name;
        let lat = resultObject.geometry.coordinates[1];
        let long = resultObject.geometry.coordinates[0];

        // add location data and list order to newly created form
        $(`#id_form-${formIndex}-name`).val(locationName);
        $(`#id_form-${formIndex}-lat`).val(lat);
        $(`#id_form-${formIndex}-long`).val(long);
        $(`#id_form-${formIndex}-order`).val(parseInt(formIndex) + 1);

        // increment total forms in management form
        $("#id_form-TOTAL_FORMS").val(parseInt(formIndex) + 1);
    }

    // create new location form on "Add" button click
    $("#add-location").click(function () {
        // check there is a location currently saved
        if (currentLocationObject != null){
            $("#locations-instructions").hide();
            $("#add-location").hide();

            // add location data to a new form
            addLocationForm(currentLocationObject);

            // clear currentLocationObject variable and map search bar
            currentLocationObject = null;
            auto.destroy();
        }
    });
});