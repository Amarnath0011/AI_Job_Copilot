import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="mt-20 border-t border-gray-200 bg-gray-50">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-6 py-8 text-center md:flex-row">
        
        {/* Logo & Description */}
        <div>
          <h2 className="text-xl font-bold text-blue-600">
            AI Job Copilot
          </h2>

          <p className="mt-2 max-w-sm text-sm text-gray-600">
            Your AI-powered assistant for Resume Analysis, ATS Optimization,
            Interview Preparation, and Career Growth.
          </p>
        </div>

        {/* Navigation Links */}
        <div className="flex gap-6 text-gray-600">
          <Link
            to="/"
            className="transition-colors duration-200 hover:text-blue-600"
          >
            Home
          </Link>

          <Link
            to="/resume"
            className="transition-colors duration-200 hover:text-blue-600"
          >
            Resume
          </Link>

          <Link
            to="/interview"
            className="transition-colors duration-200 hover:text-blue-600"
          >
            Interview
          </Link>

          <Link
            to="/report"
            className="transition-colors duration-200 hover:text-blue-600"
          >
            Report
          </Link>
        </div>

        {/* Copyright */}
        <div className="text-sm text-gray-500">
          © {new Date().getFullYear()} AI Job Copilot. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;