import { Link } from "react-router-dom";

const CTA = () => {
  return (
    <section className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 py-24">
      <div className="mx-auto max-w-5xl px-6 text-center">

        <h2 className="text-4xl font-extrabold text-white md:text-5xl">
          Ready to Land Your Dream Job?
        </h2>

        <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-blue-100">
          Upload your resume, improve your ATS score, practice AI-powered
          interviews, and build confidence before your next opportunity.
        </p>

        <div className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">

          <Link
            to="/resume"
            className="rounded-xl bg-white px-8 py-4 text-lg font-semibold text-blue-600 shadow-lg transition-all duration-300 hover:scale-105 hover:bg-gray-100"
          >
            Analyze Resume
          </Link>

          <Link
            to="/interview"
            className="rounded-xl border-2 border-white px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:scale-105 hover:bg-white hover:text-blue-600"
          >
            Start AI Interview
          </Link>

        </div>

      </div>
    </section>
  );
};

export default CTA;