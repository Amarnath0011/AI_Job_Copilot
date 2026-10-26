import Card from "../../components/ui/Card";

const LoadingScreen = ({ message }) => {
  return (
    <Card className="mx-auto max-w-3xl text-center">

      <div className="mx-auto h-16 w-16 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600"></div>

      <h2 className="mt-8 text-3xl font-bold">
        {message}
      </h2>

      <p className="mt-3 text-gray-600">
        Please wait while AI is processing...
      </p>

    </Card>
  );
};

export default LoadingScreen;