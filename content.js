// Listen for messages from the popup.js script
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    if (request.action === "getPageContent") {
        
      // Extract article information
      const title = document.title || document.querySelector('h1')?.textContent || 'No title found';
      
      // Find main content - prefer article, then main, then div with most paragraphs
      let contentElement = document.querySelector('article') || document.querySelector('main');

      if (!contentElement) {

        // Find div with most p elements
        const divs = Array.from(document.querySelectorAll('div'));
        
        contentElement = divs.reduce((max, div) => {
          const pCount = div.querySelectorAll('p').length;
          return pCount > (max ? max.querySelectorAll('p').length : 0) ? div : max;
        }, null);
      }
      
      // Extract paragraphs from content element
      const paragraphs = contentElement ? Array.from(contentElement.querySelectorAll('p')).map(p => p.textContent.trim()).filter(text => text.length > 20) : [];
      const content = paragraphs.join('\n\n');
      
      sendResponse({ 
        title: title.trim(),
        content: content || document.body.innerText.substring(0, 2000) // fallback
      });
    }
  }
);