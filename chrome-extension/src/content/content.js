// import { extractLinkedInJob } from "./extractors/linkedin";

// console.log("🚀 AI Job Copilot Content Script Loaded");

// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

//   if (message.type === "GET_JOB") {

//     sendResponse(extractLinkedInJob());

//   }

//   return true;
// });
console.log("🚀 AI Job Copilot Content Script Loaded");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received:", message);

  if (message.type === "GET_PAGE_INFO") {
    const data = {
      url: window.location.href,
      title: document.title,
    };

    console.log("Sending:", data);

    sendResponse(data);
  }

  return true;
});