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
                console.log("Page content:", response.content);

                // Display the content in the popup
                document.getElementById('contentArea').innerText = response.content.substring(0, 500) + '...';
            } else {
                document.getElementById('contentArea').innerText = 'No content received.';
            }
        });
    });
});