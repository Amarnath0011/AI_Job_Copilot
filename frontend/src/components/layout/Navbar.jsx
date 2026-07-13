import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        
        {/* Logo */}
        <Link
          to="/"
          className="text-2xl font-bold text-blue-600 hover:text-blue-700"
        >
          AI Job Copilot
        </Link>

        {/* Navigation Links */}
        <div className="hidden items-center gap-8 text-gray-700 md:flex">
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

        {/* CTA Button */}
        <Link
          to="/resume"
          className="rounded-lg bg-blue-600 px-5 py-2 font-medium text-white transition-all duration-200 hover:bg-blue-700"
        >
          Get Started
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;