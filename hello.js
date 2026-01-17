async function getCurrentTab() {
    // active: filters for the current viewed tab
    // lastFocusedWindow: restrict to only the most recent focued window
    let queryOptions = { active: true, lastFocusedWindow: true };

    // `tabs` is an array of tabs that match the query
    let [tab] = await chrome.tabs.query(queryOptions); 
    return tab;
}

// Example usage:
getCurrentTab().then(tab => {
  console.log("Current Tab URL:", tab.url);
  console.log("Current Tab Title:", tab.title);
});

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
            if (chrome.runtime.lastError) {
                console.error("Error sending message:", chrome.runtime.lastError);
                document.getElementById('contentArea').innerText = 'Error: Could not retrieve page content.';
                return;
            }

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