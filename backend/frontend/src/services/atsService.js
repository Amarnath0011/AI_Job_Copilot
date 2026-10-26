import api from "../api/axios";

export const analyzeResume = async (sessionId, jobDescription) => {
    const response = await api.post("/ats/analyze", {
        session_id: sessionId,
        job_description: jobDescription,
    });

    return response.data;
};