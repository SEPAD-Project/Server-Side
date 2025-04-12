// function for getting status
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
        
        // update button status
        updateButtonStates(data);

        setTimeout(checkApiStatus, 1000);
    } catch (error) {
        console.error('Error while getting status', error);
        setTimeout(checkApiStatus, 1000);
    }
}

// function for updating api status in html
function updateApiStatus(apiName, status) {
    const element = document.querySelector(`.${apiName}-status`);
    if (!element) return;
    
    // update text
    element.textContent = status.toUpperCase();
    
    // update class
    if (status === 'running') {
        element.classList.remove('status-stopped');
        element.classList.add('status-running');
    } else {
        element.classList.remove('status-running');
        element.classList.add('status-stopped');
    }
}

// funvtion for updating buttons
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

// function for sending requests to api
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
        
        // check again after change
        setTimeout(checkApiStatus, 500);
    } catch (error) {
        console.error(`Error in ${action} API ${apiNumber}:`, error);
    }
}

// adding event listeners for buttons
function setupButtonListeners() {
    for (let i = 1; i <= 4; i++) {
        // Start
        document.querySelector(`.btn-start${i}`).addEventListener('click', () => {
            sendApiRequest('start', i);
        });
        
        // Stop
        document.querySelector(`.btn-stop${i}`).addEventListener('click', () => {
            sendApiRequest('stop', i);
        });
        
        // Restart
        document.querySelector(`.btn-restart${i}`).addEventListener('click', () => {
            sendApiRequest('restart', i);
        });
    }
}

// start checking status event listeners
document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();
    setupButtonListeners();
});