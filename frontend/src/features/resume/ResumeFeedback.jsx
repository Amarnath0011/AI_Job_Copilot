const ResumeFeedback = ({ feedback }) => {
  return (
    <div className="space-y-8">

      <div className="rounded-xl bg-blue-50 p-6">
        <h2 className="text-2xl font-bold text-blue-700">
          Overall Feedback
        </h2>

        <p className="mt-3 text-gray-700">
          {feedback.overall_feedback}
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">

        <div className="rounded-xl border p-6">

          <h3 className="mb-4 text-xl font-semibold text-green-600">
            Strengths
          </h3>

          <ul className="list-disc space-y-2 pl-5">

            {feedback.strengths.map(item => (
              <li key={item}>{item}</li>
            ))}

          </ul>

        </div>

        <div className="rounded-xl border p-6">

          <h3 className="mb-4 text-xl font-semibold text-red-600">
            Weaknesses
          </h3>

          <ul className="list-disc space-y-2 pl-5">

            {feedback.weaknesses.map(item => (
              <li key={item}>{item}</li>
            ))}

          </ul>

        </div>

      </div>

      <div className="rounded-xl border p-6">

        <h3 className="text-xl font-semibold">
          Resume Summary
        </h3>

        <p className="mt-3">
          {feedback.resume_summary}
        </p>

      </div>

      <div className="rounded-xl border p-6 bg-green-50">

        <h3 className="text-xl font-semibold text-green-700">
          Improved Summary
        </h3>

        <p className="mt-3">
          {feedback.improved_summary}
        </p>

      </div>

      <div className="rounded-xl border p-6">

        <h3 className="mb-4 text-xl font-semibold">
          Recommended Keywords
        </h3>

        <div className="flex flex-wrap gap-3">

          {feedback.recommended_keywords.map(keyword => (
            <span
              key={keyword}
              className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700"
            >
              {keyword}
            </span>
          ))}

        </div>

      </div>

      <div className="rounded-xl border p-6">

        <h3 className="mb-4 text-xl font-semibold">
          Improvement Suggestions
        </h3>

        <ul className="list-disc space-y-3 pl-5">

          {feedback.improvement_suggestions.map(item => (
            <li key={item}>{item}</li>
          ))}

        </ul>

      </div>

    </div>
  );
};

export default ResumeFeedback;