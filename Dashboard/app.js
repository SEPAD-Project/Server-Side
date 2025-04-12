// Function to show toast notifications
function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `${type}-toast`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Remove after 3 seconds with slideOut animation
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

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
    
    element.textContent = status.toUpperCase();
    
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
        
        if (result.status === 'error') {
            showToast('error', result.message);
        } else {
            showToast('success', result.message);
        }
        
        setTimeout(checkApiStatus, 500);
    } catch (error) {
        console.error(`Error in ${action} API ${apiNumber}:`, error);
        showToast('error', `Failed to ${action} API ${apiNumber}`);
    }
}

// Function to update server metrics
function updateMetrics() {
    fetch('http://localhost:8000/metrics')
        .then(response => response.json())
        .then(metrics => {
            // Update numeric values
            document.getElementById('cpu-usage').textContent = `${metrics.cpu}%`;
            document.getElementById('memory-usage').textContent = `${metrics.memory}%`;
            document.getElementById('disk-usage').textContent = `${metrics.disk}%`;
            document.getElementById('network-usage').textContent = `${metrics.network} MB`;

            // Update gauge rotations
            document.getElementById('cpu-gauge').style.transform = 
                `rotate(${(metrics.cpu / 100) * 0.5}turn)`;
            document.getElementById('memory-gauge').style.transform = 
                `rotate(${(metrics.memory / 100) * 0.5}turn)`;

            // Update gauge labels
            document.querySelectorAll('.gauge-cover').forEach((cover, index) => {
                cover.textContent = index === 0 ? 
                    `${metrics.cpu.toFixed(1)}%` : 
                    `${metrics.memory.toFixed(1)}%`;
            });
        })
        .catch(error => {
            console.error('Error fetching metrics:', error);
            showToast('error', 'Failed to fetch server metrics');
        });
}

// Function to periodically update metrics
function startMetricsUpdates() {
    updateMetrics(); // Initial update
    setInterval(updateMetrics, 1000); // Update every second
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
    startMetricsUpdates();
});