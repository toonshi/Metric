// google_maps.js
$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function(script, textStatus) {
        google.maps.event.addDomListener(window, "load", initMap);
    });

function initMap() {
    var institutionLat = parseFloat($('#institution-lat').val()); // Get latitude of institution from hidden input field
    var institutionLng = parseFloat($('#institution-lng').val()); // Get longitude of institution from hidden input field

    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: {
            lat: institutionLat,
            lng: institutionLng
        }
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay, institutionLat, institutionLng);
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, institutionLat, institutionLng) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat_a = position.coords.latitude; // User's latitude
            var long_a = position.coords.longitude; // User's longitude

            var origin = { lat: lat_a, lng: long_a };
            var destination = { lat: institutionLat, lng: institutionLng }; // Set destination to institution's location

            directionsService.route({
                origin: origin,
                destination: destination,
                travelMode: google.maps.TravelMode.DRIVING,
            }, function(response, status) {
                if (status === 'OK') {
                    directionsDisplay.setDirections(response);
                } else {
                    alert('Directions request failed due to ' + status);
                    window.location.assign("/route");
                }
            });
        }, function(error) {
            var lat_a = parseFloat($('#id-lat-a').val()); // Get latitude of user's location
            var long_a = parseFloat($('#id-long-a').val()); // Get longitude of user's location
            console.error('Error getting user location:', error);
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
        // Handle browser not supporting geolocation
    }
}
