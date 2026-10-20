import { useState } from "react";
import { uploadResume } from "../../services/ResumeService";
import { analyzeResume } from "../../services/atsService";

const ResumeUpload = ({ onUploadSuccess, onATSAnalysis }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please select a resume.");
    if (jobDescription.trim().length < 20) return alert("Job Description must contain at least 20 characters.");

    try {
      setLoading(true);
      const uploadResponse = await uploadResume(selectedFile);
      onUploadSuccess(uploadResponse);
      const atsResponse = await analyzeResume(uploadResponse.data.session_id, jobDescription);
      onATSAnalysis(atsResponse);
      alert("ATS Analysis Completed Successfully!");
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl rounded-2xl bg-white p-8 shadow-xl">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800">Resume Analysis</h2>
        <p className="mt-2 text-gray-500">Upload your PDF resume and paste the job description to receive an AI-powered ATS analysis.</p>
      </div>
      <div className="mb-8">
        <label className="mb-2 block font-semibold text-gray-700">Resume (PDF, max 10 MB)</label>
        <input type="file" accept=".pdf,application/pdf" onChange={(event) => setSelectedFile(event.target.files?.[0] || null)} className="block w-full rounded-lg border border-gray-300 p-3 file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:font-medium file:text-white hover:file:bg-blue-700" />
        {selectedFile && <p className="mt-3 text-sm text-green-600">Selected: {selectedFile.name}</p>}
      </div>
      <div className="mb-8">
        <label className="mb-2 block font-semibold text-gray-700">Job Description</label>
        <textarea rows={10} value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste the complete Job Description here..." className="w-full rounded-lg border border-gray-300 p-4 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
      </div>
      <button onClick={handleUpload} disabled={loading} className="w-full rounded-lg bg-blue-600 py-3 text-lg font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400">{loading ? "Uploading and analyzing..." : "Analyze Resume"}</button>
    </div>
  );
};

export default ResumeUpload;
