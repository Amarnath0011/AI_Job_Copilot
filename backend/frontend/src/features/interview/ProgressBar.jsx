const ProgressBar = ({
    currentQuestion,
    totalQuestions,
  }) => {
    const progress =
      (currentQuestion / totalQuestions) * 100;
  
    return (
      <div className="mb-10">
  
        <div className="mb-3 flex justify-between">
  
          <p className="font-semibold">
            Question {currentQuestion} / {totalQuestions}
          </p>
  
          <p className="text-blue-600 font-semibold">
            {Math.round(progress)}%
          </p>
  
        </div>
  
        <div className="h-3 rounded-full bg-gray-200">
  
          <div
            className="h-3 rounded-full bg-blue-600 transition-all duration-500"
            style={{
              width: `${progress}%`,
            }}
          />
  
        </div>
  
      </div>
    );
  };
  
  export default ProgressBar;