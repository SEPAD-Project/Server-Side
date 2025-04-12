// Function for getting API status
async function checkApiStatus() {
    try {
        const response = await fetch('http://localhost:8000/status');
        const data = await response.json();
        
        console.log(`api1:${data.api1.status}`);
        console.log(`api2:${data.api2.status}`);
        console.log(`api3:${data.api3.status}`);
        console.log(`api4:${data.api4.status}`);

        updateApiStatus('api1', data.api1.status);
        updateApiStatus('api2', data.api2.status);
        updateApiStatus('api3', data.api3.status);
        updateApiStatus('api4', data.api4.status);
        
        // Update button status
        updateButtonStates(data);

        setTimeout(checkApiStatus, 1000);
    } catch (error) {
        console.error('Error while getting status', error);
        showToast('error', 'Failed to fetch API status');
        setTimeout(checkApiStatus, 1000);
    }
}

// Function for updating API status in HTML
function updateApiStatus(apiName, status) {
    const element = document.querySelector(`.${apiName}-status`);
    if (!element) return;
    
    // Update text
    element.textContent = status.toUpperCase();
    
    // Update class
    if (status === 'running') {
        element.classList.remove('status-stopped');
        element.classList.add('status-running');
    } else {
        element.classList.remove('status-running');
        element.classList.add('status-stopped');
    }
}

// Function for updating button states
function updateButtonStates(data) {
    for (let i = 1; i <= 4; i++) {
        const status = data[`api${i}`].status;
        const startBtn = document.querySelector(`.btn-start${i}`);
        const stopBtn = document.querySelector(`.btn-stop${i}`);
        const restartBtn = document.querySelector(`.btn-restart${i}`);

        if (status === 'running') {
            startBtn.disabled = true;
            stopBtn.disabled = false;
            restartBtn.disabled = false;
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
            restartBtn.disabled = true;
        }
    }
}

// Function for sending requests to API
async function sendApiRequest(action, apiNumber) {
    try {
        const url = `http://localhost:8000/${action}/${apiNumber}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        console.log(`Response for ${action} API ${apiNumber}:`, result.message);
        
        // Show toast notification based on response
        if (result.status === 'error') {
            showToast('error', result.message);
        } else {
            showToast('success', result.message);
        }
        
        // Check again after change
        setTimeout(checkApiStatus, 500);
    } catch (error) {
        console.error(`Error in ${action} API ${apiNumber}:`, error);
        showToast('error', `Failed to ${action} API ${apiNumber}`);
    }
}

// Function to show toast notifications
function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}-toast`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Add animation
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Function for adding event listeners to buttons
function setupButtonListeners() {
    for (let i = 1; i <= 4; i++) {
        // Start button
        document.querySelector(`.btn-start${i}`).addEventListener('click', () => {
            sendApiRequest('start', i);
        });
        
        // Stop button
        document.querySelector(`.btn-stop${i}`).addEventListener('click', () => {
            sendApiRequest('stop', i);
        });
        
        // Restart button
        document.querySelector(`.btn-restart${i}`).addEventListener('click', () => {
            sendApiRequest('restart', i);
        });
    }
}

// Start checking status and setup event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();
    setupButtonListeners();
});