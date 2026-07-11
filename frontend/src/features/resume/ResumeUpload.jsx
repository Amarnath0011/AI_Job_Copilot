import { useState } from "react";
import { uploadResume } from "../../services/resumeService";
import { analyzeResume } from "../../services/atsService";

const ResumeUpload = ({ onUploadSuccess, onATSAnalysis }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please upload the file.");
      return;
    }

    try {
      const uploadResponse = await uploadResume(selectedFile);

      onUploadSuccess(uploadResponse);

      const jobDescription = prompt("Enter Job Description");
      const sessionId = uploadResponse.data.session_id;

      if (!jobDescription) return;

      const atsResponse = await analyzeResume(sessionId , jobDescription);

      onATSAnalysis(atsResponse);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Resume Upload</h2>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={handleFileChange}
      />

      <button onClick={handleUpload}>
        Upload Resume
      </button>
    </div>
  );
};

export default ResumeUpload;