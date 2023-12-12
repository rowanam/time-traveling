function setMapHeight() {
    // set map aspect ratio to 3:2, based on width
    $("#map").height($("#map").width() * 2 / 3);
}

export { setMapHeight };