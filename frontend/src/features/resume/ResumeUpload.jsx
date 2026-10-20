import { useState } from "react";
import { uploadResume } from "../../services/ResumeService";
import { analyzeResume } from "../../services/atsService";

export default function ResumeUpload({ onUploadSuccess, onATSAnalysis }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleUpload(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    if (!selectedFile) return setError("Choose a PDF resume first.");
    if (!selectedFile.name.toLowerCase().endsWith(".pdf") || (selectedFile.type && selectedFile.type !== "application/pdf")) {
      return setError("Only PDF resumes are supported.");
    }
    if (jobDescription.trim().length < 20) {
      return setError("Please enter a job description with at least 20 characters.");
    }

    setLoading(true);
    try {
      const uploadResponse = await uploadResume(selectedFile);
      onUploadSuccess?.(uploadResponse);
      const sessionId = uploadResponse?.data?.session_id;
      if (!sessionId) throw new Error("The upload response did not include a resume session ID.");
      const atsResponse = await analyzeResume(sessionId, jobDescription.trim());
      onATSAnalysis?.(atsResponse);
      setSuccess("Resume securely uploaded. Your ATS analysis is ready.");
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Something went wrong. Please retry.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleUpload} className="mx-auto max-w-4xl rounded-2xl bg-white p-6 shadow-xl sm:p-8">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800">Resume Analysis</h2>
        <p className="mt-2 text-gray-500">Upload a PDF and paste the job description for an AI-powered ATS analysis.</p>
      </div>
      {error && <p role="alert" className="mb-5 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
      {success && <p role="status" className="mb-5 rounded-lg bg-green-50 p-3 text-sm text-green-700">{success}</p>}
      <div className="mb-6">
        <label htmlFor="resume-file" className="mb-2 block font-semibold text-gray-700">Resume (PDF, max 10 MB)</label>
        <input id="resume-file" type="file" accept=".pdf,application/pdf" onChange={(event) => setSelectedFile(event.target.files?.[0] || null)} className="block w-full rounded-lg border border-gray-300 p-3" />
        {selectedFile && <p className="mt-2 text-sm text-gray-600">Selected: {selectedFile.name}</p>}
      </div>
      <div className="mb-6">
        <label htmlFor="job-description" className="mb-2 block font-semibold text-gray-700">Job Description</label>
        <textarea id="job-description" rows={9} value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} placeholder="Paste the job description here..." className="w-full rounded-lg border border-gray-300 p-4 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200" />
      </div>
      <button type="submit" disabled={loading} className="w-full rounded-lg bg-blue-600 py-3 text-lg font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400">
        {loading ? "Uploading and analyzing..." : "Upload & Analyze Resume"}
      </button>
    </form>
  );
}
