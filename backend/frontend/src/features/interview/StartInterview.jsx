import Card from "../../components/ui/Card";

const StartInterview = ({ onStart }) => {
  return (
    <Card className="mx-auto mt-12 max-w-4xl text-center">

      <div className="text-7xl">
        🎤
      </div>

      <h2 className="mt-6 text-3xl font-bold">
        Ready for your Interview?
      </h2>

      <p className="mx-auto mt-4 max-w-2xl text-gray-600">
        You will be asked five adaptive interview questions based on
        your previous answers.
      </p>

      <button
        onClick={onStart}
        className="mt-10 rounded-xl bg-blue-600 px-10 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
      >
        Start Interview
      </button>

    </Card>
  );
};

export default StartInterview;