// Listen for messages from the hello.js script
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    if (request.action === "getPageContent") {
        
      // Get the whole HTML or text content
      // Use document.body.innerText for text, or document.documentElement.outerHTML for full HTML
      const pageContent = document.documentElement.outerHTML; 
      sendResponse({ content: pageContent });
    }
  }
);