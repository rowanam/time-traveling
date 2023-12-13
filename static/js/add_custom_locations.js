import {
    setMapHeight
} from './map_sizing.js';

$(document).ready(function () {
    // size map on page load and window resizing
    setMapHeight();
    $(window).resize(setMapHeight);

    // INITIALIZE VARIABLES
    let currentLocationObject = null;
    let currentCoordinates = [];
    let coordinatesArray = [];
    let polyline;

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

            const {
                display_name
            } = object.properties;
            const [lng, lat] = object.geometry.coordinates;

            // display result on map
            const marker = L.marker([lat, lng], {
                title: display_name,
            });
            marker.addTo(map).bindPopup(display_name);

            // display "Add" button
            $("#add-location").show();

            // store current location result and coordinates
            currentLocationObject = object;
            currentCoordinates = [lat, lng];

            // update coordinates array and polyline, adding selected city temporarily
            addCoordinates(currentCoordinates, true);

            // update map view
            if (polyline) {
                map.fitBounds(polyline.getBounds());
            } else {
                map.setView([lat, lng], 8);
            }
        },

        // the method presents no results element
        noResults: ({
                currentValue,
                template
            }) =>
            template(`<li>No results found: "${currentValue}"</li>`),
    });

    /**
     * Add a new form to the locations formset with data from the search result
     * @param {object} resultObject - object containing geographical results data
     */
    function addLocationForm(resultObject) {
        // get current total number of forms, which will be the next form index
        let formIndex = $("#id_form-TOTAL_FORMS").val();

        // add a new form to list - html content of empty-form with correct index added to id and name attributes
        let formCopy = $("#empty-form").html().replace(/__prefix__/g, formIndex);
        $("#locations-list").append(`<li class="location-form">${formCopy}</li>`);

        // change display of list item, label and icon
        let nameInput = $(`#id_form-${formIndex}-name`);
        nameInput.prev("label").hide();
        nameInput.before("<span class='pin-icon'><i class='fa-solid fa-map-pin'></i></span>");
        nameInput.after(`
            <div class="dropdown location-dropdown ms-auto">
                <i class="fa-solid fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                <ul class="dropdown-menu">
                    <li>
                        <span class="dropdown-item">
                        <i class="fa-solid fa-pen mx-2"></i> Edit name
                        </span>
                    </li>
                    <li>
                        <span class="dropdown-item">
                        <i class="fa-solid fa-arrow-rotate-right mx-2"></i> Change location
                        </span>
                    </li>
                    <li>
                        <span class="dropdown-item">
                            <i class="fa-solid fa-trash mx-2"></i> Delete
                        </span>
                    </li>
                </ul>
            </div>
        `);
        nameInput.attr("class", "location-hidden-display");

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

    /**
     * Add coordinates from the current location to the coordinates sequence
     * @param {array} coordinates - an array containing a lat and a long coordinate
     * @param {boolean} temp - whether the new coordinates should be added temporarily
     */
    function addCoordinates(coordinates, temp) {
        // add new coordinates to array
        coordinatesArray.push(coordinates);

        updatePolyline();

        // if coordinates added temporarliy, remove them.
        // this is done if a city is selected from the list to view,
        // but not yet added to the trip
        if (temp) {
            coordinatesArray.pop();
        }
    }

    /**
     * Move a pair of coordinates in coordinatesArray to a new position
     * @param {number} oldIndex - original index of coordinates
     * @param {number} newIndex - new index of coordinates 
     */
    function moveCoordinates(oldIndex, newIndex) {
        // move coordinates from old to new position
        let movedCoordinates = coordinatesArray.splice(oldIndex, 1)[0];
        coordinatesArray.splice(newIndex, 0, movedCoordinates);

        updatePolyline();
    }

    /**
     * Update the polyline on the map
     */
    function updatePolyline() {
        // only display polylines if there are at least 2 points
        if (coordinatesArray.length >= 2) {
            // remove any existing polyline
            if (polyline) {
                polyline.remove();
            }

            // create and display a polyline from the coordinates array
            polyline = L.polyline(coordinatesArray, {
                color: 'orange',
                weight: 2,
            }).addTo(map);
        }
    }

    // create new location form on "Add" button click
    $("#add-location").click(function () {
        // check there is a location currently saved
        if (currentLocationObject != null) {
            $("#locations-instructions").hide();
            $("#add-location").hide();

            // add location data to a new form
            addLocationForm(currentLocationObject);

            // clear currentLocationObject variable and map search bar
            currentLocationObject = null;
            auto.destroy();

            addCoordinates(currentCoordinates, false);
        }
    });

    // make locations list sortable
    $("#locations-list").sortable({
        update: function (event, ui) {
            let originalOrder = $("> p > input[id$='-order']", ui.item).attr("value");

            // start locations ordering at 1
            let order = 1;

            // when user changes order, update "order" in each location form
            $("#locations-list > li").each(function () {
                $("> p > input[id$='-order']", this).attr("value", order);
                order++;
            });

            let newOrder = $("> p > input[id$='-order']", ui.item).attr("value");

            // update coordinates sequence and polyline on map
            moveCoordinates(originalOrder - 1, newOrder - 1);
        }
    });
});