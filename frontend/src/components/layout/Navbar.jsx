import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const user = (() => {
    try { return JSON.parse(localStorage.getItem("auth_user") || "null"); }
    catch { return null; }
  })();

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("auth_user");
    navigate("/login", { replace: true });
  }

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to="/" className="text-xl font-bold text-blue-600 hover:text-blue-700">AI Job Copilot</Link>
        <div className="flex items-center gap-4 text-sm text-gray-700 sm:gap-6">
          <Link to="/" className="hover:text-blue-600">Home</Link>
          {token && <>
            <Link to="/dashboard" className="hover:text-blue-600">Dashboard</Link>
            <Link to="/resume" className="hover:text-blue-600">Resume</Link>
            <Link to="/interview" className="hover:text-blue-600">Interview</Link>
            <Link to="/report" className="hover:text-blue-600">Report</Link>
          </>}
        </div>
        {token
          ? <div className="flex items-center gap-3">
              {user?.full_name && <span className="hidden text-sm text-slate-600 md:inline">{user.full_name}</span>}
              <button onClick={logout} className="rounded-lg border border-slate-300 px-3 py-2 font-medium text-slate-700 hover:bg-slate-100">Log out</button>
            </div>
          : <Link to="/login" className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700">Log in / Sign up</Link>}
      </div>
    </nav>
  );
}
