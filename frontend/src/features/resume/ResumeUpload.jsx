import { useState } from "react";
import { uploadResume } from "../../services/resumeService";
import { analyzeResume } from "../../services/atsService";

const ResumeUpload = ({ onUploadSuccess, onATSAnalysis }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a resume.");
      return;
    }

    if (jobDescription.trim().length < 20) {
      alert("Job Description must contain at least 20 characters.");
      return;
    }

    try {
      setLoading(true);

      // Step 1: Upload Resume
      const uploadResponse = await uploadResume(selectedFile);

      onUploadSuccess(uploadResponse);

      // Step 2: Get Session ID
      const sessionId = uploadResponse.data.session_id;

      // Step 3: Analyze ATS
      const atsResponse = await analyzeResume(
        sessionId,
        jobDescription
      );

      onATSAnalysis(atsResponse);

      alert("ATS Analysis Completed Successfully!");
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl rounded-2xl bg-white p-8 shadow-xl">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800">
          Resume Analysis
        </h2>
  
        <p className="mt-2 text-gray-500">
          Upload your resume and paste the job description to receive
          an AI-powered ATS analysis.
        </p>
      </div>
  
      {/* Resume Upload */}
      <div className="mb-8">
        <label className="mb-2 block font-semibold text-gray-700">
          Resume
        </label>
  
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="block w-full rounded-lg border border-gray-300 p-3
                     file:mr-4
                     file:rounded-md
                     file:border-0
                     file:bg-blue-600
                     file:px-4
                     file:py-2
                     file:font-medium
                     file:text-white
                     hover:file:bg-blue-700"
        />
  
        {selectedFile && (
          <p className="mt-3 text-sm text-green-600">
            Selected File: {selectedFile.name}
          </p>
        )}
      </div>
  
      {/* Job Description */}
      <div className="mb-8">
        <label className="mb-2 block font-semibold text-gray-700">
          Job Description
        </label>
  
        <textarea
          rows={10}
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the complete Job Description here..."
          className="w-full rounded-lg border border-gray-300 p-4
                     focus:border-blue-500
                     focus:outline-none
                     focus:ring-2
                     focus:ring-blue-200"
        />
      </div>
  
      {/* Button */}
      <button
        onClick={handleUpload}
        disabled={loading}
        className="w-full rounded-lg bg-blue-600 py-3 text-lg font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
      >
        {loading ? "Analyzing Resume..." : "Analyze Resume"}
      </button>
    </div>
  );

}

export default ResumeUpload;