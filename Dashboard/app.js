// function for getting status
async function checkApiStatus() {
    try {
        const response = await fetch('http://localhost:8000/status');
        const data = await response.json();
        
        console.log(`api1:${data.api1.status}`);
        console.log(`api2:${data.api2.status}`);
        console.log(`api3:${data.api3.status}`);
        console.log(`api4:${data.api4.status}`);
        

        setTimeout(checkApiStatus, 1000);
    } catch (error) {
        console.error('Error while getting status', error);
        setTimeout(checkApiStatus, 1000);
    }
}

// start checking
checkApiStatus();