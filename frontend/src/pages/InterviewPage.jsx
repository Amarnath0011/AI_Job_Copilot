import { useState } from "react";

import InterviewHeader from "../features/interview/InterviewHeader";
import StartInterview from "../features/interview/StartInterview";
import ProgressBar from "../features/interview/ProgressBar";
import QuestionCard from "../features/interview/QuestionCard";
import AnswerInput from "../features/interview/AnswerInput";
import ScoreCard from "../features/interview/ScoreCard";
import LoadingScreen from "../features/interview/LoadingScreen";
import InterviewComplete from "../features/interview/InterviewComplete";
import { useNavigate } from "react-router-dom";
import { startInterview , submitAnswer , endInterview } from "../services/InterviewService";

const InterviewPage = () => {
  const navigate = useNavigate();
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [completed, setCompleted] = useState(false);

  const [jobDescription, setJobDescription] = useState("");

  const [sessionId, setSessionId] = useState("");

  const [question, setQuestion] = useState("");

  const [currentQuestion, setCurrentQuestion] = useState(1);

  const [totalQuestions, setTotalQuestions] = useState(5);

  const [evaluation, setEvaluation] = useState(null);

  const handleStartInterview = async () => {
    if (jobDescription.trim().length < 20) {
      alert("Job Description must contain at least 20 characters.");
      return;
    }

    try {
      setLoading(true);

      const response = await startInterview(jobDescription);

      setSessionId(response.data.session_id);

      setQuestion(response.data.question);

      setCurrentQuestion(response.data.question_number);

      setTotalQuestions(response.data.total_questions);

      setStarted(true);
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail ||
          "Unable to start interview."
      );
    } finally {
      setLoading(false);
    }
  };
  const handleSubmitAnswer = async (answer) => {
    try {
      setLoading(true);
  
      const response = await submitAnswer(sessionId, answer);
  
      const data = response.data;
  
      setEvaluation(data.evaluation);
  
      if (data.interview_completed) {
  
        const reportResponse = await endInterview(sessionId);
  
        navigate("/report", {
          state: {
            report: reportResponse.data,
          },
        });
  
        return;
      }
  
      setQuestion(data.next_question);
  
      setCurrentQuestion(data.question_number);
  
      setTotalQuestions(data.total_questions);
  
    } catch (error) {
      console.error(error);
  
      alert(
        error.response?.data?.detail ||
        "Unable to submit answer."
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <LoadingScreen message="Preparing your AI Interview..." />
      </div>
    );
  }

  if (completed) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <InterviewComplete />
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="mx-auto max-w-7xl px-6">

        <InterviewHeader />

        {!started ? (
          <div className="mx-auto mt-12 max-w-5xl rounded-2xl bg-white p-8 shadow-lg">

            <h2 className="mb-4 text-2xl font-bold">
              Job Description
            </h2>

            <textarea
              rows={10}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste Job Description Here..."
              className="w-full rounded-xl border border-gray-300 p-4 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            />

            <div className="mt-8">
              <StartInterview
                onStart={handleStartInterview}
              />
            </div>

          </div>
        ) : (
          <div className="mt-12 grid gap-8 lg:grid-cols-3">

            {/* Left Section */}

            <div className="space-y-8 lg:col-span-2">

              <ProgressBar
                currentQuestion={currentQuestion}
                totalQuestions={totalQuestions}
              />

              <QuestionCard
                question={question}
              />

              <AnswerInput
                loading={loading}
                onSubmit={handleSubmitAnswer}
              />

            </div>

            {/* Right Section */}

            <div>

            {evaluation && (
            <ScoreCard
                evaluation={evaluation}
            />
)}

            </div>

          </div>
        )}

      </div>
    </div>
  );
};

export default InterviewPage;