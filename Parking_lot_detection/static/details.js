// details.js for details.html
let lotNumber;

document.addEventListener('DOMContentLoaded', function() {
    // Get lot number from URL
    const urlParams = new URLSearchParams(window.location.search);
    lotNumber = urlParams.get('lot');
    
    // Update page title
    document.getElementById('lot-title').textContent = `Parking Lot ${lotNumber} Details`;
    
    // Update date and time
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Fetch parking data periodically
    fetchDetailData();
    setInterval(fetchDetailData, 5000);
    
    // Set up video stream
    setupVideoStream();
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

function fetchDetailData() {
    // In a real application, this would make an API call to your backend
    // For now, we'll simulate with a fetch to a hypothetical endpoint
    
    fetch(`/api/parking-details?lot=${lotNumber}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateDetailUI(data);
        })
        .catch(error => {
            console.error('Error fetching parking details:', error);
            // For demo/development, use mock data when API is not available
            const mockData = {
                total: lotNumber === '1' ? 25 : 30,
                available: lotNumber === '1' ? 12 : 8,
                occupied: lotNumber === '1' ? 13 : 22
            };
            updateDetailUI(mockData);
        });
}

function updateDetailUI(data) {
    document.getElementById('detail-total').textContent = data.total;
    document.getElementById('detail-available').textContent = data.available;
    document.getElementById('detail-occupied').textContent = data.occupied;
}

function setupVideoStream() {
    // In a real application, this would connect to a video stream from your backend
    // For now, we'll simulate with a static image or placeholder
    
    const videoFeed = document.getElementById('video-feed');
    
    // Try to connect to a stream - in production this would be a real stream URL
    videoFeed.src = `/api/video-stream?lot=${lotNumber}`;
    
    // Handle errors by showing a placeholder
    videoFeed.onerror = function() {
        videoFeed.src = `/placeholder-${lotNumber}.jpg`;
        videoFeed.alt = "Video stream unavailable";
    };
}

function goBack() {
    window.location.href = "/";
}