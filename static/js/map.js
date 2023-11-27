// Initialize and add the map
let map;

async function initMap() {
    // The location of Uluru
    const position = {
        lat: -25.344,
        lng: 131.031
    };
    // Request needed libraries.
    //@ts-ignore
    const {
        Map
    } = await google.maps.importLibrary("maps");
    const {
        AdvancedMarkerElement
    } = await google.maps.importLibrary("marker");

    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 3,
        center: {
            lat: 0,
            lng: -180
        },
        mapTypeId: "terrain",
    });

    const flightPlanCoordinates = [{
            lat: 37.772,
            lng: -122.214
        },
        {
            lat: 21.291,
            lng: -157.821
        },
        {
            lat: -18.142,
            lng: 178.431
        },
        {
            lat: -27.467,
            lng: 153.027
        },
    ];
    const flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    flightPath.setMap(map);
}

initMap();