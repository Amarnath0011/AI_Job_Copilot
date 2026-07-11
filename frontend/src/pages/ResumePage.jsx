import { useState } from "react";

import ResumeUpload from "../features/resume/ResumeUpload";
import ATSScore from "../features/resume/ATSScore";
import ResumeFeedback from "../features/resume/ResumeFeedback";

const ResumePage = () => {
  const [resumeData, setResumeData] = useState(null);
  const [atsData, setATSData] = useState(null);

  return (
    <div>
      <h1>Resume Analysis</h1>

      <ResumeUpload
        onUploadSuccess={setResumeData}
        onATSAnalysis={setATSData}
      />

      <ATSScore data={atsData} />

      <ResumeFeedback data={atsData} />
    </div>
  );
};

export default ResumePage;