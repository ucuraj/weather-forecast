// [START maps_event_click_latlng]

let lat;
let lon;

function initMap() {
    const myLatlng = {lat: -34.9163, lng: -58.9634};
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 4,
        center: myLatlng,
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map to get Lat/Lng!",
        position: myLatlng,
    });

    infoWindow.open(map);
    // [START maps_event_click_latlng_listener]
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        });
        infoWindow.setContent(
            JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        );

        lat = mapsMouseEvent.latLng.lat().toFixed(4);
        lon = mapsMouseEvent.latLng.lng().toFixed(4);
        infoWindow.open(map);
    });
    // [END maps_event_click_latlng_listener]
}

// [END maps_event_click_latlng]