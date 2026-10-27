export function extractLinkedInJob() {
    const title =
      document.querySelector(".job-details-jobs-unified-top-card__job-title")
        ?.innerText || "";
  
    const company =
      document.querySelector(".job-details-jobs-unified-top-card__company-name")
        ?.innerText || "";
  
    const location =
      document.querySelector(".job-details-jobs-unified-top-card__primary-description-container")
        ?.innerText || "";
  
    const description =
      document.querySelector(".jobs-description-content__text")
        ?.innerText || "";
  
    return {
      title,
      company,
      location,
      description,
    };
  }