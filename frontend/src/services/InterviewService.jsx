import api from "../api/axios";

export const startInterview = async (jobDescription) => {
  const response = await api.post("/interview/start", {
    job_description: jobDescription,
  });

  return response.data;
};

export const submitAnswer = async (sessionId, answer) => {
  const response = await api.post("/interview/answer", {
    session_id: sessionId,
    answer,
  });

  return response.data;
};

export const endInterview = async (sessionId) => {
  const response = await api.post("/interview/end", {
    session_id: sessionId,
  });

  return response.data;
};