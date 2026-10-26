import StrengthCard from "./StrengthCard";
import WeaknessCard from "./WeaknessCard";

const FinalReport = ({ report }) => {
  const scores = [
    {
      title: "Overall",
      value: report.overall_score,
      color: "text-blue-600",
    },
    {
      title: "Technical",
      value: report.technical_score,
      color: "text-green-600",
    },
    {
      title: "Communication",
      value: report.communication_score,
      color: "text-yellow-600",
    },
    {
      title: "Problem Solving",
      value: report.problem_solving_score,
      color: "text-purple-600",
    },
    {
      title: "Confidence",
      value: report.confidence_score,
      color: "text-pink-600",
    },
  ];

  return (
    <div className="space-y-10">

      {/* Header */}

      <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-700 p-10 text-white shadow-xl">

        <h1 className="text-4xl font-bold">
          AI Interview Report
        </h1>

        <p className="mt-4 text-blue-100">
          Your personalized interview performance analysis.
        </p>

      </div>

      {/* Scores */}

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-5">

        {scores.map((item) => (
          <div
            key={item.title}
            className="rounded-2xl bg-white p-6 shadow-lg"
          >
            <p className="text-gray-500">
              {item.title}
            </p>

            <h2
              className={`mt-3 text-5xl font-bold ${item.color}`}
            >
              {item.value}
            </h2>
          </div>
        ))}

      </div>

      {/* Summary */}

      <div className="rounded-2xl bg-white p-8 shadow-lg">

        <h2 className="text-2xl font-bold">
          Interview Summary
        </h2>

        <p className="mt-5 leading-8 text-gray-700">
          {report.summary}
        </p>

      </div>

      {/* Strengths & Weaknesses */}

      <div className="grid gap-8 lg:grid-cols-2">

        <StrengthCard
          strengths={report.strengths}
        />

        <WeaknessCard
          weaknesses={report.weaknesses}
        />

      </div>

      {/* Knowledge Gaps */}

      {report.knowledge_gaps.length > 0 && (
        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-6 text-2xl font-bold">
            Knowledge Gaps
          </h2>

          <ul className="space-y-4">

            {report.knowledge_gaps.map((gap) => (
              <li
                key={gap}
                className="rounded-xl bg-red-50 p-4"
              >
                {gap}
              </li>
            ))}

          </ul>

        </div>
      )}

      {/* Learning Roadmap */}

      <div className="rounded-2xl bg-white p-8 shadow-lg">

        <h2 className="mb-6 text-2xl font-bold">
          Learning Roadmap
        </h2>

        <ul className="space-y-4">

          {report.learning_roadmap.map((item) => (
            <li
              key={item}
              className="rounded-xl bg-blue-50 p-4"
            >
              {item}
            </li>
          ))}

        </ul>

      </div>

      {/* Question Feedback */}

      <div className="rounded-2xl bg-white p-8 shadow-lg">

        <h2 className="mb-8 text-2xl font-bold">
          Question-wise Feedback
        </h2>

        <div className="space-y-6">

          {report.question_feedback.map((item, index) => (

            <div
              key={index}
              className="rounded-xl border border-gray-200 p-6"
            >

              <h3 className="text-xl font-semibold">
                Question {index + 1}
              </h3>

              <p className="mt-4 font-medium text-gray-700">
                {item.question}
              </p>

              <div className="mt-4">

                <span className="rounded-lg bg-blue-100 px-4 py-2 font-semibold text-blue-700">
                  Score : {item.score}
                </span>

              </div>

              <div className="mt-6">

                <h4 className="font-semibold">
                  Feedback
                </h4>

                <p className="mt-2 text-gray-600">
                  {item.feedback}
                </p>

              </div>

              <div className="mt-6">

                <h4 className="font-semibold">
                  Ideal Answer Summary
                </h4>

                <p className="mt-2 text-gray-600">
                  {item.ideal_answer_summary}
                </p>

              </div>

            </div>

          ))}

        </div>

      </div>

      {/* Recommendation */}

      <div className="rounded-2xl border border-green-200 bg-green-50 p-8 text-center">

        <h2 className="text-3xl font-bold text-green-700">
          Hiring Recommendation
        </h2>

        <p className="mt-5 text-2xl font-semibold">
          {report.hiring_recommendation}
        </p>

      </div>

      {/* Difficulty */}

      <div className="rounded-2xl bg-white p-8 shadow-lg text-center">

        <h2 className="text-2xl font-bold">
          Interview Difficulty
        </h2>

        <p className="mt-4 text-xl text-gray-700">
          {report.difficulty_level}
        </p>

      </div>

    </div>
  );
};

export default FinalReport;