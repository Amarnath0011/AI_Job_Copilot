import { useState } from "react";
import Card from "../../components/ui/Card";

const AnswerInput = ({ onSubmit, loading }) => {
  const [answer, setAnswer] = useState("");

  const handleSubmit = () => {
    if (!answer.trim()) {
      alert("Please enter your answer.");
      return;
    }

    onSubmit(answer);
    setAnswer("");
  };

  return (
    <Card>

      <h2 className="mb-4 text-2xl font-bold">
        Your Answer
      </h2>

      <textarea
        rows={8}
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder="Write your answer here..."
        className="w-full rounded-xl border border-gray-300 p-4 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-6 w-full rounded-xl bg-blue-600 py-4 text-lg font-semibold text-white transition hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Evaluating..." : "Submit Answer"}
      </button>

    </Card>
  );
};

export default AnswerInput;