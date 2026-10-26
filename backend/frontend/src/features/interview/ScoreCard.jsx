import Card from "../../components/ui/Card";

const ScoreCard = ({ evaluation }) => {
  if (!evaluation) return null;

  return (
    <Card>

      <h2 className="mb-6 text-2xl font-bold">
        AI Evaluation
      </h2>

      <div className="grid gap-5 md:grid-cols-2">

        <div className="rounded-xl bg-blue-50 p-5">
          <p className="text-gray-600">
            Overall Score
          </p>

          <h3 className="mt-2 text-4xl font-bold text-blue-600">
            {evaluation.overall_score}
          </h3>
        </div>

        <div className="rounded-xl bg-green-50 p-5">
          <p className="text-gray-600">
            Technical Score
          </p>

          <h3 className="mt-2 text-4xl font-bold text-green-600">
            {evaluation.technical_score}
          </h3>
        </div>

        <div className="rounded-xl bg-yellow-50 p-5">
          <p className="text-gray-600">
            Communication
          </p>

          <h3 className="mt-2 text-4xl font-bold text-yellow-600">
            {evaluation.communication_score}
          </h3>
        </div>

        <div className="rounded-xl bg-purple-50 p-5">
          <p className="text-gray-600">
            Problem Solving
          </p>

          <h3 className="mt-2 text-4xl font-bold text-purple-600">
            {evaluation.problem_solving_score}
          </h3>
        </div>

      </div>

      <div className="mt-8">

        <h3 className="text-xl font-semibold">
          Feedback
        </h3>

        <p className="mt-3 leading-7 text-gray-600">
          {evaluation.feedback}
        </p>

      </div>

    </Card>
  );
};

export default ScoreCard;