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
        

        setTimeout(checkApiStatus, 1000);
    } catch (error) {
        console.error('Error while getting status', error);
        setTimeout(checkApiStatus, 1000);
    }
}


function updateApiStatus(apiName, status) {
    const element = document.querySelector(`.${apiName}-status`);
    if (!element) return;
    
    // update text
    element.textContent = status.toUpperCase();
    
    // update class name
    if (status === 'running') {
        element.classList.remove('status-stopped');
        element.classList.add('status-running');
    } else {
        element.classList.remove('status-running');
        element.classList.add('status-stopped');
    }
}

// start checking
document.addEventListener('DOMContentLoaded', checkApiStatus);