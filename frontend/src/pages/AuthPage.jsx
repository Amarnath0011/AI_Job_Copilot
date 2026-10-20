import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import api from "../api/axios";

export default function AuthPage() {
  const [params] = useSearchParams();
  const isSignup = params.get("mode") === "signup";
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await api.post(isSignup ? "/auth/signup" : "/auth/login", {
        ...(isSignup ? { full_name: fullName } : {}),
        email: email.trim().toLowerCase(),
        password,
      });
      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("auth_user", JSON.stringify(response.data.user));
      navigate("/resume", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to authenticate. Check the API and database.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-[75vh] bg-slate-50 px-4 py-12">
      <section className="mx-auto max-w-md rounded-2xl bg-white p-8 shadow-lg">
        <h1 className="text-3xl font-bold text-slate-900">{isSignup ? "Create your account" : "Welcome back"}</h1>
        <p className="mt-2 text-slate-600">{isSignup ? "Start managing your career with AI Job Copilot." : "Log in to access your saved resume and interview sessions."}</p>
        {error && <p role="alert" className="mt-5 rounded-lg bg-red-50 p-3 text-sm text-red-700">{String(error)}</p>}
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          {isSignup && <label className="block text-sm font-medium text-slate-700">Full name<input required minLength={2} maxLength={120} autoComplete="name" value={fullName} onChange={(e) => setFullName(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-3" /></label>}
          <label className="block text-sm font-medium text-slate-700">Email<input required type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-3" /></label>
          <label className="block text-sm font-medium text-slate-700">Password<input required type="password" minLength={isSignup ? 8 : 1} maxLength={72} autoComplete={isSignup ? "new-password" : "current-password"} value={password} onChange={(e) => setPassword(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-3" /><span className="mt-1 block text-xs text-slate-500">{isSignup ? "Use at least 8 characters." : "Your password is never stored in plain text."}</span></label>
          <button disabled={loading} className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:opacity-60">{loading ? "Please wait..." : isSignup ? "Create account" : "Log in"}</button>
        </form>
        <p className="mt-6 text-sm text-slate-600">{isSignup ? "Already registered?" : "New to AI Job Copilot?"} <Link className="font-semibold text-blue-600 hover:underline" to={isSignup ? "/login" : "/login?mode=signup"}>{isSignup ? "Log in" : "Create an account"}</Link></p>
      </section>
    </main>
  );
}
