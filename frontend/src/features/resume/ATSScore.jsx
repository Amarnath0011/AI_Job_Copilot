const ATSScore = ({
  score,
  similarity,
  matchingSkills,
  missingSkills,
}) => {
  return (
    <div className="space-y-8">

      <div className="grid gap-6 md:grid-cols-2">

        <div className="rounded-xl bg-blue-50 p-6 text-center shadow">
          <h2 className="text-lg font-semibold text-gray-600">
            ATS Score
          </h2>

          <p className="mt-3 text-6xl font-bold text-blue-600">
            {score}
          </p>
        </div>

        <div className="rounded-xl bg-green-50 p-6 shadow">
          <h2 className="text-lg font-semibold text-gray-700">
            Semantic Similarity
          </h2>

          <div className="mt-5 h-4 rounded-full bg-gray-200">

            <div
              className="h-4 rounded-full bg-green-500"
              style={{
                width: `${similarity * 100}%`,
              }}
            />

          </div>

          <p className="mt-3 text-xl font-bold">
            {(similarity * 100).toFixed(0)}%
          </p>

        </div>

      </div>

      <div className="grid gap-6 md:grid-cols-2">

        <div className="rounded-xl border p-6">

          <h3 className="mb-4 text-xl font-semibold text-green-600">
            Matching Skills
          </h3>

          <div className="flex flex-wrap gap-3">

            {matchingSkills.map(skill => (
              <span
                key={skill}
                className="rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-700"
              >
                {skill}
              </span>
            ))}

          </div>

        </div>

        <div className="rounded-xl border p-6">

          <h3 className="mb-4 text-xl font-semibold text-red-600">
            Missing Skills
          </h3>

          <div className="flex flex-wrap gap-3">

            {missingSkills.map(skill => (
              <span
                key={skill}
                className="rounded-full bg-red-100 px-4 py-2 text-sm font-medium text-red-700"
              >
                {skill}
              </span>
            ))}

          </div>

        </div>

      </div>

    </div>
  );
};

export default ATSScore;