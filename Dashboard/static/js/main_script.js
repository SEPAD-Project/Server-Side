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

// Object to store previous logs for each API
const apiLogsHistory = {
    1: '',
    2: '',
    3: '',
    4: ''
};

// Function to display logs in the container (appends new logs)
function displayLogs(apiNumber, newLogs) {
    const logContainer = document.querySelector(`.log${apiNumber}`);
    if (!logContainer) return;
    
    // Skip if no new logs
    if (!newLogs || newLogs.trim() === '') return;
    
    // Add new logs to history
    apiLogsHistory[apiNumber] += (apiLogsHistory[apiNumber] ? '\n' : '') + newLogs;
    
    // Clear container and re-render all logs
    logContainer.innerHTML = '';
    
    // Split all logs by newlines and create log entries
    const logEntries = apiLogsHistory[apiNumber].split('\n').filter(entry => entry.trim() !== '');
    
    logEntries.forEach(entry => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        // Color code based on log type
        if (entry.includes('404')) {
            logEntry.classList.add('log-error');
        } else if (entry.includes('200')) {
            logEntry.classList.add('log-success');
        } else if (entry.includes('WARNING')) {
            logEntry.classList.add('log-warning');
        } else {
            logEntry.classList.add('log-info');
        }
        
        logEntry.textContent = entry;
        logContainer.appendChild(logEntry);
    });
    
    // Auto-scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Function to check and fetch API logs
async function checkApiLogs(apiNumber) {
    try {
        const response = await fetch(`http://185.4.28.110:800/get_api_logs?api_number=${apiNumber}`);
        const data = await response.json();
        
        if (data.success && data.message) {
            console.log(`New logs received for API ${apiNumber}`);
            displayLogs(apiNumber, data.message);
        } else if (!data.success) {
            console.log(`API ${apiNumber} logs not available`);
            // Don't clear existing logs, just show status
            const statusEntry = document.createElement('div');
            statusEntry.className = 'log-entry log-warning';
            statusEntry.textContent = `[${new Date().toLocaleTimeString()}] Logs not available - ${data.message}`;
            document.querySelector(`.log${apiNumber}`).appendChild(statusEntry);
        }
    } catch (error) {
        console.error(`Error fetching logs for API ${apiNumber}:`, error);
        // Don't clear existing logs, just show error
        const errorEntry = document.createElement('div');
        errorEntry.className = 'log-entry log-error';
        errorEntry.textContent = `[${new Date().toLocaleTimeString()}] Error loading logs: ${error.message}`;
        document.querySelector(`.log${apiNumber}`).appendChild(errorEntry);
    }
}

// Function for getting API status
async function checkApiStatus() {
    try {
        const response = await fetch('http://185.4.28.110:800/status');
        const data = await response.json();
        
        // Log API statuses
        console.log(`api1:${data.api1.status}`);
        console.log(`api2:${data.api2.status}`);
        console.log(`api3:${data.api3.status}`);
        console.log(`api4:${data.api4.status}`);

        // Update UI with API statuses
        updateApiStatus('api1', data.api1.status);
        updateApiStatus('api2', data.api2.status);
        updateApiStatus('api3', data.api3.status);
        updateApiStatus('api4', data.api4.status);
        
        // Update button states
        updateButtonStates(data);

        // Check logs for running APIs
        if (data.api1.status === 'running') checkApiLogs(1);
        if (data.api2.status === 'running') checkApiLogs(2);
        if (data.api3.status === 'running') checkApiLogs(3);
        if (data.api4.status === 'running') checkApiLogs(4);

        // Check again after 1 second
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
        const url = `http://185.4.28.110:800/${action}/${apiNumber}`;
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
    fetch('http://185.4.28.110:800/metrics')
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

// Clear logs when API is stopped
function clearApiLogs(apiNumber) {
    apiLogsHistory[apiNumber] = '';
    const logContainer = document.querySelector(`.log${apiNumber}`);
    if (logContainer) {
        logContainer.innerHTML = '';
    }
}

// Start checking status and setup event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize log containers
    for (let i = 1; i <= 4; i++) {
        clearApiLogs(i);
    }
    
    checkApiStatus();
    setupButtonListeners();
    startMetricsUpdates();
});