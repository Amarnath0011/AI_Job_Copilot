import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("auth_user");
    navigate("/login", { replace: true });
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700">AI Job Copilot</Link>
        <div className="hidden items-center gap-8 text-gray-700 md:flex">
          <Link to="/" className="transition-colors hover:text-blue-600">Home</Link>
          {token && <>
            <Link to="/resume" className="transition-colors hover:text-blue-600">Resume</Link>
            <Link to="/interview" className="transition-colors hover:text-blue-600">Interview</Link>
            <Link to="/report" className="transition-colors hover:text-blue-600">Report</Link>
          </>}
        </div>
        {token
          ? <button onClick={logout} className="rounded-lg border border-slate-300 px-4 py-2 font-medium text-slate-700 hover:bg-slate-100">Log out</button>
          : <Link to="/login" className="rounded-lg bg-blue-600 px-5 py-2 font-medium text-white transition-all hover:bg-blue-700">Log in / Sign up</Link>}
      </div>
    </nav>
  );
};

export default Navbar;
