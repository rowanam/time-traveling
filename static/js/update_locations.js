$(document).ready(function () {

    // -------------------- SET UP FORMS --------------------

    // move forms with "name" fields of "_to_delete_" to deleted forms list
    // so that if page reloads because form submission failed, deleted forms will be re-hidden
    $("#locations-list > li").each(function () {
        let nameField = $(" input[id$='-name']", this)[0];
        if ($(nameField).val() == "_to_delete_") {
            $("#deleted-locations").append($(this));
        }
    });

    // remove "required" attribute from empty form to prevent form submission error
    $("#id_locations-__prefix__-name").removeAttr("required");

    // -------------------- DISPLAY FUNCTIONS --------------------

    /**
     * Show or hide location adding instructions depending on whether locations list is empty
     */
    function updateInstructionsDisplay() {
        if ($("#locations-list > li").length > 0) {
            $("#locations-instructions").hide();
        } else {
            $("#locations-instructions").show();
        }
    }

    /**
     * Disable location adding button if locations list is empty
     */
    function updateSubmitButtonDisable() {
        if ($("#locations-list > li").length == 0) {
            $("#save-locations-button").prop("disabled", true);
        } else {
            $("#save-locations-button").prop("disabled", false);
        }
    }

    /**
     * Change the display of a location item:
     * hide the label, add a pin that allows draggable reordering,
     * and control options menu
     * @param {number} formIndex - the formset index value of the form
     */
    function changeLocationItemDisplay(formIndex) {
        // get the name input field of a displayed form
        let nameInput = $(`#id_locations-${formIndex}-name`);

        // hide label
        nameInput.prev("label").hide();

        // add pin icon and dropdown controls menu elements
        nameInput.before("<span class='pin-icon'><i class='fa-solid fa-map-pin'></i></span>");
        nameInput.after(`
            <div class="dropdown location-dropdown ms-auto">
                <i class="fa-solid fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                <ul class="dropdown-menu">
                    <li>
                        <span class="dropdown-item delete-location-control">
                            <i class="fa-solid fa-trash mx-2"></i> Delete
                        </span>
                    </li>
                </ul>
            </div>
        `);

        // add styling class to name input field
        nameInput.attr("class", "location-hidden-display");
    }

    /**
     * Set map height - aspect ratio 3:2, based on width
     */
    function setMapHeight() {
        $("#map").height($("#map").width() * 2 / 3);
    }

    // -------------------- SET UP DISPLAY --------------------
    // size map on page load and window resizing
    setMapHeight();
    $(window).resize(setMapHeight);

    // show instructions and disable submit button if there are no locations
    updateInstructionsDisplay();
    updateSubmitButtonDisable();

    // update displays for existing location item forms
    for (let i = 0; i < $("#id_locations-INITIAL_FORMS").val(); i++) {
        changeLocationItemDisplay(i);
    }

    // get initial coordinates (passed from view)
    let initialCoordinates = JSON.parse($("#initialCoordinates").text());

    // -------------------- INITIALIZE VARIABLES --------------------
    let currentLocationObject = null;
    let currentCoordinates = [];
    let coordinatesArray = initialCoordinates;
    let polyline;

    // -------------------- DISPLAY MAP --------------------
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

    // -------------------- ADD AUTOCOMPLETE SEARCH BAR --------------------
    const auto = new Autocomplete("search", {
        // default selects the first item in
        // the list of results
        selectFirst: true,

        // the number of characters entered should start searching
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

    // -------------------- MAP DISPLAY FUNCTIONS --------------------

    /**
     * Update polyline on the map
     */
    function updatePolyline() {
        // remove any existing polyline
        if (polyline) {
            polyline.remove();
        }

        // only display polylines if there are at least 2 points
        if (coordinatesArray.length >= 2) {
            // create and display a polyline from the coordinates array
            polyline = L.polyline(coordinatesArray, {
                color: 'orange',
                weight: 2,
            }).addTo(map);

            // update map view
            map.fitBounds(polyline.getBounds());
        }
    }

    // -------------------- SET UP MAP DISPLAY --------------------
    // display the initial polyline (if there are locations)
    updatePolyline();

    // -------------------- LOCATION FORMS FUNCTIONS --------------------

    /**
     * Add a new form to the locations formset with data from the search result
     * @param {object} resultObject - object containing geographical results data
     */
    function addLocationForm(resultObject) {
        // get current total number of forms, which will be the next form index
        let formIndex = $("#id_locations-TOTAL_FORMS").val();

        // add a new form to list - html content of empty-form with correct index added to id and name attributes
        let formCopy = $("#empty-form").html().replace(/__prefix__/g, formIndex);
        $("#locations-list").append(`<li class="location-form">${formCopy}</li>`);

        // change display of list item, label and icon
        changeLocationItemDisplay(formIndex);

        // get results from map search and store location name and coordinate data
        let locationName = resultObject.properties.name;
        let lat = resultObject.geometry.coordinates[1];
        let long = resultObject.geometry.coordinates[0];

        // add location data and list order to newly created form
        $(`#id_locations-${formIndex}-name`).val(locationName);
        $(`#id_locations-${formIndex}-lat`).val(lat);
        $(`#id_locations-${formIndex}-long`).val(long);

        let order = $("#locations-list > li").length
        $(`#id_locations-${formIndex}-order`).val(order);

        // set name field "required" attribute
        $(`#id_locations-${formIndex}-name`).attr("required", "required");

        // increment total forms in management form
        $("#id_locations-TOTAL_FORMS").val(parseInt(formIndex) + 1);
    }

    /**
     * Reset "order" fields on all location forms, numbered starting from 1
     */
    function reorderLocations() {
        let order = 1;
        $("#locations-list > li").each(function () {
            $("> p > input[id$='-order']", this).val(order);
            order++;
        });
    }

    // -------------------- COORDINATES SEQUENCE FUNCTIONS --------------------

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
     * Delete a pair of coordinates from coordinatesArray
     * @param {number} index - index of the coordinates to be removed
     */
    function deleteCoordinates(index) {
        coordinatesArray.splice(index, 1);
        updatePolyline();
    }

    // -------------------- EVENT HANDLERS --------------------

    // change display and create new location form on "Add" button click
    $("#add-location").click(function () {
        // check there is a location currently saved from map search
        if (currentLocationObject != null) {
            $("#locations-instructions").hide();
            $("#add-location").hide();

            // add location data to a new form
            addLocationForm(currentLocationObject);

            updateSubmitButtonDisable();

            // clear currentLocationObject variable and map search bar
            currentLocationObject = null;
            auto.destroy();

            // clear the map
            map.eachLayer(function (layer) {
                if (!!layer.toGeoJSON) {
                    map.removeLayer(layer);
                }
            });

            // add coordinates to locations array and diplay polyline
            addCoordinates(currentCoordinates, false);
        }
    });

    // make locations list sortable
    $("#locations-list").sortable({
        // when user drops an item in a new position
        // reset all items' "order" fields and update polyline coordinates sequence
        update: function (event, ui) {
            let originalOrder = $("> p > input[id$='-order']", ui.item).val();
            reorderLocations();
            let newOrder = $("> p > input[id$='-order']", ui.item).val();

            // update coordinates sequence and polyline on map
            moveCoordinates(originalOrder - 1, newOrder - 1);
        }
    });

    // delete location on button click
    // event listener added to list so listeners don't need to be
    // created/removed for each location addition/deletion
    $("#locations-list").click(function (e) {
        if (e.target && e.target.matches("span.delete-location-control")) {
            // get the locations form li
            let formLI = $(e.target).parents("li.location-form")[0];

            let order = $("input[id$='-order']", formLI).val();
            deleteCoordinates(order - 1);

            // set the delete input field to "checked"
            let deleteField = $(" input[id$='-DELETE']", formLI)[0];
            $(deleteField).val("checked");

            // move the form li into deleted-locations list to hide it
            // moved into separate list so ordering isn't affected
            $("#deleted-locations").append($(formLI));

            // set name field to "_to_delete_"
            // (to prevent empty field from messing up form submission)
            let nameField = $(" input[id$='-name']", formLI)[0]
            $(nameField).val("_to_delete_");

            reorderLocations();

            updateInstructionsDisplay();
            updateSubmitButtonDisable();
        }
    });
});