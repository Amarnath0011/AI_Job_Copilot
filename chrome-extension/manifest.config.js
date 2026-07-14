const manifest = {
    manifest_version: 3,
  
    name: "AI Job Copilot",
  
    version: "1.0.0",
  
    description: "AI-powered ATS Analyzer",
  
    action: {
      default_popup: "index.html",
      default_title: "AI Job Copilot",
    },
  
    permissions: [
      "storage",
      "activeTab",
      "scripting"
    ],
  
    host_permissions: [
      "<all_urls>"
    ],
  };
  
  export default manifest;