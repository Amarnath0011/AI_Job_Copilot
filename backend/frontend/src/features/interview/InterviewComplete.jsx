import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";

const InterviewComplete = () => {
  return (
    <Card className="mx-auto max-w-4xl text-center">

      <div className="text-7xl">
        🎉
      </div>

      <h2 className="mt-6 text-4xl font-bold">
        Interview Completed
      </h2>

      <p className="mx-auto mt-5 max-w-2xl text-gray-600">
        Congratulations! Your interview has been completed successfully.
        You can now view your final AI-generated performance report.
      </p>

      <Link
        to="/report"
        className="mt-10 inline-block rounded-xl bg-blue-600 px-10 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
      >
        View Final Report
      </Link>

    </Card>
  );
};

export default InterviewComplete;