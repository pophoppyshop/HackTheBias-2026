async function postData(url, data) {
  try {
    // Pause until a response is received
    const response = await fetch(url, {
      method: 'POST', // Specify the method
      headers: {
        'Content-Type': 'application/json' // Inform the server the body format
      },
      body: JSON.stringify(data) // Convert the JavaScript object to a JSON string
    });

    // Check for HTTP errors
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const responseData = await response.json(); // Parse the response to a usuable JavaScript object
    console.log('Success:', responseData);

    // Display whether article is biased and justification
    const displayText = `
<strong>Title:</strong> <br> ${responseData.title || 'N/A'}<br><br>
<strong>Result:</strong><br>${responseData.result || 'No results extracted'}`;

    document.getElementById('contentArea').innerHTML = displayText;
  } catch (error) {
    console.error('Error:', error);

    document.getElementById('contentArea').innerHTML = error;
  }
}


// Query for the active tab in the current window
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const tabId = tabs[0].id;

    // First, inject the content script
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        files: ['content.js']
    }, () => {
        // After injection, send the message
        chrome.tabs.sendMessage(tabId, { action: "getPageContent" }, function(response) {

            // Send error if content can't be extracted
            if (chrome.runtime.lastError) {
                console.error("Error sending message:", chrome.runtime.lastError);

                document.getElementById('contentArea').innerText = 'Error: Could not retrieve page content.';

                return;
            }

            // Show content snippet if received
            if (response && response.content) {
                // Prepare url and data for POST request
                const apiEndpoint = 'https://hackthebias-2026.onrender.com/items/';
                const dataToSend = {
                    "Title": response.title,
                    "Content": response.content
                }

                // Post data to API
                const postResponse = postData(apiEndpoint, dataToSend);

                console.log("Waiting for response:", postResponse);
            } else {
                document.getElementById('contentArea').innerText = 'No results received.';
            }
        });
    });
});

// Add event listener for expand button
document.getElementById('expandBtn').addEventListener('click', () => {
    document.body.classList.toggle('expanded');
});

// Add event listener for accessibility button
document.getElementById('accessibilityBtn').addEventListener('click', () => {
    document.body.classList.toggle('large-font');
});