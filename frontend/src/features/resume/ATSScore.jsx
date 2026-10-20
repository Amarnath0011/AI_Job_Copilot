const ATSScore = ({
  score,
  similarity,
  keywordScore,
  matchingSkills = [],
  missingSkills = [],
}) => {
  const keywordCoverage =
    typeof keywordScore === "number" ? `${keywordScore.toFixed(0)}%` : "N/A";

  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-3">
        <div className="rounded-xl bg-blue-50 p-6 text-center shadow">
          <h2 className="text-lg font-semibold text-gray-600">ATS Score</h2>
          <p className="mt-3 text-6xl font-bold text-blue-600">{score}</p>
          <p className="mt-2 text-sm text-gray-500">Weighted match score out of 100</p>
        </div>

        <div className="rounded-xl bg-green-50 p-6 shadow">
          <h2 className="text-lg font-semibold text-gray-700">Keyword Coverage</h2>
          <div className="mt-5 h-4 rounded-full bg-gray-200">
            <div
              className="h-4 rounded-full bg-green-500"
              style={{ width: `${typeof keywordScore === "number" ? Math.max(0, Math.min(100, keywordScore)) : 0}%` }}
            />
          </div>
          <p className="mt-3 text-xl font-bold">{keywordCoverage}</p>
          <p className="mt-1 text-sm text-gray-600">
            {typeof keywordScore === "number"
              ? "Recognized JD skills found in your resume"
              : "No supported skills were detected in the job description"}
          </p>
        </div>

        <div className="rounded-xl bg-purple-50 p-6 shadow">
          <h2 className="text-lg font-semibold text-gray-700">Semantic Similarity</h2>
          <div className="mt-5 h-4 rounded-full bg-gray-200">
            <div
              className="h-4 rounded-full bg-purple-500"
              style={{ width: `${Math.max(0, Math.min(100, (similarity || 0) * 100))}%` }}
            />
          </div>
          <p className="mt-3 text-xl font-bold">
            {((similarity || 0) * 100).toFixed(0)}%
          </p>
          <p className="mt-1 text-sm text-gray-600">Meaning-level text similarity, not a hiring probability</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border p-6">
          <h3 className="mb-4 text-xl font-semibold text-green-600">Matching Skills</h3>
          {matchingSkills.length ? (
            <div className="flex flex-wrap gap-3">
              {matchingSkills.map((skill) => (
                <span key={skill} className="rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-700">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No supported skills matched.</p>
          )}
        </div>

        <div className="rounded-xl border p-6">
          <h3 className="mb-4 text-xl font-semibold text-red-600">Missing Skills</h3>
          {missingSkills.length ? (
            <div className="flex flex-wrap gap-3">
              {missingSkills.map((skill) => (
                <span key={skill} className="rounded-full bg-red-100 px-4 py-2 text-sm font-medium text-red-700">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No missing skills from the supported skill dictionary.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ATSScore;
