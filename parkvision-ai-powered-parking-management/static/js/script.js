// script.js for index.html
document.addEventListener('DOMContentLoaded', function() {
    // Update date and time
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Fetch parking data periodically
    fetchParkingData();
    setInterval(fetchParkingData, 5000);
});

function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('datetime').textContent = now.toLocaleDateString('en-US', options);
}

function fetchParkingData() {
    // In a real application, this would make an API call to your backend
    // For now, we'll simulate with a fetch to a hypothetical endpoint
    
    // Using fetch API to get data from our Python backend
    fetch('/api/parking-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateParkingUI(data);
        })
        .catch(error => {
            console.error('Error fetching parking data:', error);
            // For demo/development, use mock data when API is not available
            const mockData = {
                lot1: {
                    total: 25,
                    available: 12,
                    occupied: 13
                },
                lot2: {
                    total: 30,
                    available: 8,
                    occupied: 22
                }
            };
            updateParkingUI(mockData);
        });
}

function updateParkingUI(data) {
    // Update Lot 1
    if (data.lot1) {
        document.getElementById('lot1-total').textContent = data.lot1.total;
        document.getElementById('lot1-available').textContent = data.lot1.available;
        document.getElementById('lot1-occupied').textContent = data.lot1.occupied;
    }
    
    // Update Lot 2
    if (data.lot2) {
        document.getElementById('lot2-total').textContent = data.lot2.total;
        document.getElementById('lot2-available').textContent = data.lot2.available;
        document.getElementById('lot2-occupied').textContent = data.lot2.occupied;
    }
}

function navigateToDetails(lotNumber) {
    window.location.href = `details.html?lot=${lotNumber}`;
}