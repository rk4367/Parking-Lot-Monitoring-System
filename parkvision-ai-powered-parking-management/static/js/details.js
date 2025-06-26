// details.js - Optimized for better video streaming performance
let lotNumber;
let videoRetryCount = 0;
const MAX_RETRY_COUNT = 3;

document.addEventListener('DOMContentLoaded', function() {
    // Get lot number from URL
    const urlParams = new URLSearchParams(window.location.search);
    lotNumber = urlParams.get('lot');
    
    // Update page title
    document.getElementById('lot-title').textContent = `Parking Lot ${lotNumber} Details`;
    
    // Update date and time
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Fetch parking data with optimized intervals
    fetchDetailData();
    setInterval(fetchDetailData, 3000); // Reduced from 5000ms to 3000ms
    
    // Set up video stream with retry mechanism
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
            // Fallback to mock data for development
            const mockData = {
                total: lotNumber === '1' ? 25 : 30,
                available: lotNumber === '1' ? 12 : 8,
                occupied: lotNumber === '1' ? 13 : 22
            };
            updateDetailUI(mockData);
        });
}

function updateDetailUI(data) {
    // Smooth number transitions
    animateNumber('detail-total', data.total);
    animateNumber('detail-available', data.available);
    animateNumber('detail-occupied', data.occupied);
}

function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    const currentValue = parseInt(element.textContent) || 0;
    
    if (currentValue !== targetValue) {
        const increment = targetValue > currentValue ? 1 : -1;
        const duration = 300; // 300ms animation
        const steps = Math.abs(targetValue - currentValue);
        const stepDuration = duration / Math.max(steps, 1);
        
        let current = currentValue;
        const timer = setInterval(() => {
            current += increment;
            element.textContent = current;
            
            if (current === targetValue) {
                clearInterval(timer);
            }
        }, stepDuration);
    }
}

function setupVideoStream() {
    const videoFeed = document.getElementById('video-feed');
    const videoWrapper = document.querySelector('.video-wrapper');
    
    // Create loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.innerHTML = `
        <div class="spinner"></div>
        <p>Loading video stream...</p>
    `;
    loadingIndicator.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: white;
        z-index: 10;
    `;
    
    // Add CSS for spinner
    const style = document.createElement('style');
    style.textContent = `
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .video-error {
            background-color: #e74c3c;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
        }
        
        .retry-button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        
        .retry-button:hover {
            background-color: #2980b9;
        }
    `;
    document.head.appendChild(style);
    
    videoWrapper.appendChild(loadingIndicator);
    
    // Optimized video stream setup
    const streamUrl = `/api/video-stream?lot=${lotNumber}&t=${Date.now()}`;
    
    videoFeed.onload = function() {
        // Remove loading indicator when video loads
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.remove();
        }
        videoRetryCount = 0; // Reset retry count on successful load
        console.log(`Video stream loaded successfully for lot ${lotNumber}`);
    };
    
    videoFeed.onerror = function() {
        console.error(`Video stream error for lot ${lotNumber}`);
        handleVideoError();
    };
    
    // Set up video stream with cache busting
    videoFeed.src = streamUrl;
    
    // Retry mechanism for failed streams
    function retryVideoStream() {
        if (videoRetryCount < MAX_RETRY_COUNT) {
            videoRetryCount++;
            console.log(`Retrying video stream (attempt ${videoRetryCount}/${MAX_RETRY_COUNT})`);
            
            // Add loading indicator back
            if (!document.querySelector('.loading-indicator')) {
                videoWrapper.appendChild(loadingIndicator);
            }
            
            // Retry with new timestamp
            setTimeout(() => {
                videoFeed.src = `/api/video-stream?lot=${lotNumber}&t=${Date.now()}`;
            }, 2000 * videoRetryCount); // Exponential backoff
        } else {
            showVideoError();
        }
    }
    
    function handleVideoError() {
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.remove();
        }
        retryVideoStream();
    }
    
    function showVideoError() {
        // Remove loading indicator
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.remove();
        }
        
        // Show error message with retry button
        const errorDiv = document.createElement('div');
        errorDiv.className = 'video-error';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Video Stream Unavailable</h3>
            <p>Unable to load video stream for Parking Lot ${lotNumber}</p>
            <button class="retry-button" onclick="retryVideoManually()">
                <i class="fas fa-sync-alt"></i> Retry
            </button>
        `;
        
        videoWrapper.appendChild(errorDiv);
        videoFeed.style.display = 'none';
    }
    
    // Make retry function global
    window.retryVideoManually = function() {
        const errorDiv = document.querySelector('.video-error');
        if (errorDiv) {
            errorDiv.remove();
        }
        
        videoFeed.style.display = 'block';
        videoRetryCount = 0;
        setupVideoStream(); // Restart the setup process
    };
    
    // Periodic health check for video stream
    setInterval(() => {
        // Check if video element is still receiving data
        if (videoFeed.complete && videoFeed.naturalWidth === 0) {
            console.log('Video stream health check failed, attempting recovery...');
            handleVideoError();
        }
    }, 10000); // Check every 10 seconds
}

function goBack() {
    window.location.href = "/";
}

// Add visibility change handler to pause/resume video when tab is not active
document.addEventListener('visibilitychange', function() {
    const videoFeed = document.getElementById('video-feed');
    if (document.hidden) {
        // Page is hidden, could pause video updates
        console.log('Page hidden, video continues in background');
    } else {
        // Page is visible, ensure video is working
        console.log('Page visible, checking video stream');
        if (videoFeed && videoFeed.src && videoFeed.complete && videoFeed.naturalWidth === 0) {
            // Video might be stuck, refresh it
            const currentSrc = videoFeed.src;
            videoFeed.src = currentSrc.split('&t=')[0] + '&t=' + Date.now();
        }
    }
});