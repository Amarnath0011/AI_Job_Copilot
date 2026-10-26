import Card from "../../components/ui/Card";

const QuestionCard = ({ question }) => {
  return (
    <Card>

      <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-600">
        Current Question
      </span>

      <h2 className="mt-6 text-2xl font-bold leading-10 text-gray-900">
        {question}
      </h2>

    </Card>
  );
};

export default QuestionCard;