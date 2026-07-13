import { useState } from "react";

import ResumeUpload from "../features/resume/ResumeUpload";
import ATSScore from "../features/resume/ATSScore";
import ResumeFeedback from "../features/resume/ResumeFeedback";

const ResumePage = () => {
  const [resumeData, setResumeData] = useState(null);
  const [atsData, setATSData] = useState(null);
  const [activeTab, setActiveTab] = useState("ats");

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="mx-auto max-w-7xl px-6 py-12">

        {/* Heading */}
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-900">
            Resume Analysis
          </h1>

          <p className="mt-3 text-lg text-gray-600">
            Upload your resume, paste a Job Description, and get an
            AI-powered ATS analysis with personalized feedback.
          </p>
        </div>

        {/* Resume Upload Card */}
        <div className="mb-10 rounded-2xl bg-white p-8 shadow-lg">
          <ResumeUpload
            onUploadSuccess={setResumeData}
            onATSAnalysis={setATSData}
          />
        </div>

        {atsData && (
          <>
            {/* Score Section */}
            <div className="mb-10 grid gap-6 lg:grid-cols-2">

              <div className="rounded-2xl bg-white p-6 shadow-lg">
                <ATSScore
                  score={atsData.data.ats_score}
                  similarity={atsData.data.semantic_similarity}
                  matchingSkills={atsData.data.matching_skills}
                  missingSkills={atsData.data.missing_skills}
                />
              </div>

              {/* Quick Stats */}
              <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h2 className="mb-5 text-2xl font-semibold">
                  Quick Overview
                </h2>

                <div className="space-y-5">

                  <div className="rounded-lg bg-green-50 p-4">
                    <h3 className="font-semibold text-green-700">
                      Matching Skills
                    </h3>

                    <p className="mt-2 text-3xl font-bold">
                      {atsData.data.matching_skills.length}
                    </p>
                  </div>

                  <div className="rounded-lg bg-red-50 p-4">
                    <h3 className="font-semibold text-red-700">
                      Missing Skills
                    </h3>

                    <p className="mt-2 text-3xl font-bold">
                      {atsData.data.missing_skills.length}
                    </p>
                  </div>

                </div>
              </div>
            </div>

            {/* Feedback Section */}
            <div className="mt-10 rounded-2xl bg-white shadow-lg overflow-hidden">

<div className="flex border-b">

  <button
    onClick={() => setActiveTab("ats")}
    className={`flex-1 p-4 font-semibold transition ${
      activeTab === "ats"
        ? "bg-blue-600 text-white"
        : "bg-white hover:bg-gray-100"
    }`}
  >
    ATS Analysis
  </button>

  <button
    onClick={() => setActiveTab("feedback")}
    className={`flex-1 p-4 font-semibold transition ${
      activeTab === "feedback"
        ? "bg-blue-600 text-white"
        : "bg-white hover:bg-gray-100"
    }`}
  >
    Resume Feedback
  </button>

</div>

<div className="p-8">

  {activeTab === "ats" ? (
    <ATSScore
      score={atsData.data.ats_score}
      similarity={atsData.data.semantic_similarity}
      matchingSkills={atsData.data.matching_skills}
      missingSkills={atsData.data.missing_skills}
    />
  ) : (
    <ResumeFeedback
      feedback={atsData.data.ai_feedback}
    />
  )}

</div>

</div>
          </>
        )}
      </div>
    </div>
  );
};

export default ResumePage;