import { useState } from "react";

function App() {
  const [pageInfo, setPageInfo] = useState(null);

  const getPageInfo = async () => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    chrome.tabs.sendMessage(
      tab.id,
      { type: "GET_PAGE_INFO" },
      (response) => {
        console.log("Popup received:", response);
    
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError);
          return;
        }
    
        setPageInfo(response);
      }
    );
  };

  return (
    <div style={{ width: 350, padding: 20 }}>
      <h2>AI Job Copilot</h2>

      <button onClick={getPageInfo}>
        Get Current Page
      </button>

      {pageInfo && (
        <div style={{ marginTop: 20 }}>
          <p>
            <strong>Title:</strong>
          </p>

          <p>{pageInfo.title}</p>

          <p>
            <strong>URL:</strong>
          </p>

          <p>{pageInfo.url}</p>
          <p>{pageInfo.title}</p>
          <p>{pageInfo.company}</p>
          <p>{pageInfo.location}</p>
          <p>{pageInfo.description}</p>
        </div>
      )}
    </div>
  );
}

export default App;