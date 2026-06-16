document.addEventListener("DOMContentLoaded", () => {
    let userLat = null, userLng = null;
    let userMarker;
    let supplierMarker;
    let vehicleMarker;
    let routeLayer;
    let animationInterval;

    let map = L.map('map').setView([21.9750, 96.0836], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    function updateMarker(lat, lng) {
        if (userMarker) {
            userMarker.setLatLng([lat, lng]);
        } else {
            userMarker = L.marker([lat, lng], { draggable: true }).addTo(map);

            userMarker.on("dragend", function (event) {
                let newPos = event.target.getLatLng();
                userLat = newPos.lat;
                userLng = newPos.lng;
                document.getElementById("action-btn").innerText = "✅ Confirm";
            });
        }
        map.setView([lat, lng], 13);
        document.getElementById("action-btn").innerText = "✅ Confirm";
        updateStep(2);
    }

    window.handleAction = function () {
        if (document.getElementById("action-btn").innerText.includes("Confirm")) {
            confirmLocation();
        } else {
            useCurrentLocation();
        }
    };

    window.useCurrentLocation = function () {
        navigator.geolocation.getCurrentPosition(
            position => {
                userLat = position.coords.latitude;
                userLng = position.coords.longitude;
                updateMarker(userLat, userLng);
            },
            error => {
                alert("Failed to get location.");
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
    };

    window.confirmLocation = function () {
        if (!userLat || !userLng) {
            alert("Please select a location first.");
            return;
        }

        document.getElementById("action-btn").innerText = "✅ Confirmed";
        getNearestSupplier(userLat, userLng);
        updateStep(3);
        document.getElementById("action-btn").innerText = "❌ Cancel Request";
    };

    window.cancelRequest = function () {
        clearInterval(animationInterval);

        if (vehicleMarker) vehicleMarker.remove();
        if (supplierMarker) supplierMarker.remove();
        if (routeLayer) routeLayer.remove();

        document.getElementById("supplier-info").innerHTML = "Request canceled.";
        document.getElementById("eta-display").innerText = "";

        document.getElementById("action-btn").innerText = "📍 Use My Location";
        updateStep(1);
    };

    function getNearestSupplier(lat, lng) {
        fetch(`http://127.0.0.1:8000/api/nearest_supplier/?lat=${lat}&lng=${lng}`)

            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Error from API:", data.error);
                    alert("Error: " + data.error);
                } else {
                    console.log("Nearest Supplier:", data);

                    if (supplierMarker) {
                        map.removeLayer(supplierMarker);
                    }

                    supplierMarker = L.marker([data.latitude, data.longitude]).addTo(map);
                    supplierMarker.bindPopup(`<b>${data.name}</b><br>Distance: ${data.distance_km} km<br>ETA: ${data.time_min} min`).openPopup();

                    let bounds = L.latLngBounds([
                        [lat, lng],
                        [data.latitude, data.longitude]
                    ]);
                    map.fitBounds(bounds);

                    getORSRoute(lat, lng, data.latitude, data.longitude);

                    if (userMarker) {
                        map.removeLayer(userMarker);
                    }

                    userMarker = L.marker([lat, lng]).addTo(map);
                    userMarker.bindPopup(`<b>Your Location</b>`).openPopup();

                    // ✅ Show supplier data popup after confirming location
                    showSupplierPopup(data.name, data.phone, data.distance_km, data.time_min);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("Error fetching supplier data.");
            });
    }

    function showSupplierPopup(name, phone, distance, eta) {
        let popup = document.createElement("div");
        popup.id = "supplier-popup";
        popup.innerHTML = `
            <div class="popup-content">
                <h2>🚛 Supplier Details</h2>
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Phone:</strong> <a href="tel:${phone}">${phone}</a></p>
                <p><strong>Distance:</strong> ${distance} km</p>
                <p><strong>ETA:</strong> ${eta} min</p>
                <button onclick="closePopup()">Close</button>
            </div>
        `;
        document.body.appendChild(popup);
    }

    window.closePopup = function () {
        let popup = document.getElementById("supplier-popup");
        if (popup) {
            document.body.removeChild(popup);
        }
    };

    const ORS_API_KEY = '5b3ce3597851110001cf6248fa758f9a5d454265b38cbe1e5947d01b';

    function getORSRoute(startLat, startLng, endLat, endLng) {
        const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${ORS_API_KEY}&start=${startLng},${startLat}&end=${endLng},${endLat}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.features && data.features.length > 0) {
                    const coordinates = data.features[0].geometry.coordinates;
                    drawRoute(coordinates);
                    animateVehicle(coordinates);
                } else {
                    alert("Failed to get route. Check ORS API key.");
                    console.error("ORS API Error:", data);
                }
            })
            .catch(error => console.error("Error fetching route:", error));
    }

    function drawRoute(coords) {
        if (routeLayer) map.removeLayer(routeLayer);

        let latlngs = coords.map(c => [c[1], c[0]]);
        routeLayer = L.polyline(latlngs, { color: "blue", weight: 5, smoothFactor: 1.5 }).addTo(map);
    }

    function animateVehicle(coords, speed = 20) {
        if (vehicleMarker) vehicleMarker.remove();

        let vehicleIcon = L.icon({
            iconUrl: "/static/images/mm.png",
            iconSize: [40, 40]
        });

        vehicleMarker = L.marker([coords[0][1], coords[0][0]], { icon: vehicleIcon }).addTo(map);

        let step = 0;
        let steps = coords.length;
        let timePerStep = (1000 * 3.6) / speed;

        animationInterval = setInterval(() => {
            if (step >= steps) {
                clearInterval(animationInterval);
                notifyUserArrival();
                return;
            }

            let lat = coords[step][1];
            let lng = coords[step][0];
            vehicleMarker.setLatLng([lat, lng]);

            step++;
        }, timePerStep);
    }

    function notifyUserArrival() {
        clearInterval(animationInterval);

        setTimeout(() => {
            alert("🚀 Your supplier has arrived!");
            window.location.href = "/";
        }, 2000);
    }

    function updateStep(step) {
        document.querySelectorAll(".step").forEach(s => s.classList.remove("active"));
        document.getElementById("step" + step).classList.add("active");
    }
});
