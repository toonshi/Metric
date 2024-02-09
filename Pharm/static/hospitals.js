
        const DEFAULT_LOCATION = { lat: 40.7128, lng: -74.0060 };
        const DEFAULT_ZOOM = 10;

        let map;
        let userLocation;

        // Sample institutions data
        const institutions = [
            { id: 1, name: 'Hospital A', location: { lat: 40.7128, lng: -74.0060 }, reviews: ['Review 1A', 'Review 2A', 'Review 3A'] },
            { id: 2, name: 'Hospital B', location: { lat: 40.7123, lng: -74.0050 }, reviews: ['Review 1B', 'Review 2B', 'Review 3B'] },
            { id: 3, name: 'Hospital C', location: { lat: 40.7130, lng: -74.0055 }, reviews: ['Review 1C', 'Review 2C', 'Review 3C'] }
        ];

        // Function to initialize Google Map
        function initMap() {
            if (!google || !google.maps) {
                handleMapLoadError();
                return;
            }

            getUserLocation()
                .then(location => {
                    userLocation = location;
                    initializeMap(userLocation);
                    findNearbyHospitals(userLocation);
                    renderInstitutionsList(); // Render list of institutions after map is initialized
                })
                .catch(handleLocationError);
        }

        // Function to handle error when Google Maps fails to load
        function handleMapLoadError() {
            console.error("Google Maps failed to load.");
            alert("Error: Google Maps failed to load. Using fallback mechanism.");

            initializeMap(DEFAULT_LOCATION);
            createMarkersForInstitutions();
            renderInstitutionsList();
        }

        // Function to get user's current location
        function getUserLocation() {
            return new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        position => resolve({ lat: position.coords.latitude, lng: position.coords.longitude }),
                        reject
                    );
                } else {
                    reject("Geolocation not supported");
                }
            });
        }

        // Function to initialize the map
        function initializeMap(location) {
            map = new google.maps.Map(document.getElementById('map'), {
                center: location,
                zoom: DEFAULT_ZOOM
            });
        }

        // Function to handle error in getting user's location
        function handleLocationError(error) {
            console.error("Error getting user location:", error);
            alert("Error: Unable to get your location. Using default location.");
            handleMapLoadError();
        }

        // Function to create markers for sample institutions
        function createMarkersForInstitutions() {
            institutions.forEach(institution => {
                const marker = new google.maps.Marker({
                    position: institution.location,
                    map: map,
                    title: institution.name
                });

                marker.addListener('click', () => {
                    const reviewsContainer = $('#reviewsContainer');
                    reviewsContainer.empty(); // Clear previous content

                    institution.reviews.forEach(review => {
                        const reviewItem = $('<div></div>').text(review);
                        reviewsContainer.append(reviewItem);
                    });

                    $('#reviewsSection').fadeIn();
                });
            });
        }

        // Function to render the list of institutions
        const renderInstitutionsList = () => {
            const listContainer = $('#map').after('<ul id="institutionsList"></ul>');
            institutions.forEach(institution => {
                const listItem = $('<li></li>').text(institution.name);
                listItem.click(() => {
                    const reviewsContainer = $('#reviewsContainer');
                    reviewsContainer.empty(); // Clear previous content

                    institution.reviews.forEach(review => {
                        const reviewItem = $('<div></div>').text(review);
                        reviewsContainer.append(reviewItem);
                    });

                    $('#reviewsSection').fadeIn();
                });
                $('#institutionsList').append(listItem);
            });

            // Attach event listener to the review form submission
            $('#reviewForm').submit(function(event) {
                event.preventDefault();
                const reviewText = $('#reviewText').val();
                if (reviewText.trim() === '') {
                    alert('Please enter a review.');
                    return;
                }

                // Here you can handle the submission of the review, e.g., sending it to a server
                alert('Review submitted successfully: ' + reviewText);
                $('#reviewText').val(''); // Clear the review input field after submission
            });
        };