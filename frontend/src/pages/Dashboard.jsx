import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Dashboard() {
  const [resumes, setResumes] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [resumeResponse, sessionResponse] = await Promise.all([
        api.get("/resume/mine"),
        api.get("/interview/sessions"),
      ]);
      setResumes(resumeResponse.data.data || []);
      setSessions(sessionResponse.data.data || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load your dashboard. Please retry.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  async function deleteSession(sessionId) {
    if (!window.confirm("Delete this interview session and its saved history?")) return;
    try {
      await api.delete(`/interview/sessions/${sessionId}`);
      setSessions((current) => current.filter((item) => item.session_id !== sessionId));
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete this session.");
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Your dashboard</h1>
            <p className="mt-2 text-slate-600">Your resumes and interview history, private to your account.</p>
          </div>
          <Link to="/resume" className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700">Analyze a resume</Link>
        </div>
        {error && <p role="alert" className="mb-5 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        {loading ? <p className="rounded-xl bg-white p-8 text-slate-600 shadow-sm">Loading your data...</p> : (
          <div className="grid gap-6 lg:grid-cols-2">
            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <div className="mb-5 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-slate-900">Saved resumes</h2>
                <span className="rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700">{resumes.length}</span>
              </div>
              {resumes.length === 0 ? <p className="text-slate-500">No resume uploaded yet. Upload a PDF to start.</p> : (
                <ul className="divide-y divide-slate-100">
                  {resumes.map((resume) => <li key={resume.resume_id} className="py-4">
                    <p className="font-medium text-slate-900">{resume.filename}</p>
                    <p className="mt-1 break-all text-xs text-slate-500">Session: {resume.session_id}</p>
                    {resume.created_at && <p className="mt-1 text-xs text-slate-500">{new Date(resume.created_at).toLocaleString()}</p>}
                  </li>)}
                </ul>
              )}
            </section>
            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <div className="mb-5 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-slate-900">Interview sessions</h2>
                <span className="rounded-full bg-violet-50 px-3 py-1 text-sm text-violet-700">{sessions.length}</span>
              </div>
              {sessions.length === 0 ? <p className="text-slate-500">Your completed and in-progress interviews will appear here.</p> : (
                <ul className="divide-y divide-slate-100">
                  {sessions.map((session) => <li key={session.session_id} className="flex items-start justify-between gap-4 py-4">
                    <div>
                      <p className="font-medium text-slate-900">{session.is_completed ? "Completed interview" : "Interview in progress"}</p>
                      <p className="mt-1 text-sm text-slate-600">Question {Math.min(session.question_number, session.total_questions)} of {session.total_questions} · Average score {session.average_score}/100</p>
                      {session.created_at && <p className="mt-1 text-xs text-slate-500">{new Date(session.created_at).toLocaleString()}</p>}
                    </div>
                    <button onClick={() => deleteSession(session.session_id)} className="shrink-0 rounded-lg border border-red-200 px-3 py-2 text-sm text-red-700 hover:bg-red-50">Delete</button>
                  </li>)}
                </ul>
              )}
            </section>
          </div>
        )}
      </div>
    </main>
  );
}
