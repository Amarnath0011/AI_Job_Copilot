import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";

const Hero = () => {
  return (
    <section className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="mx-auto flex min-h-[90vh] max-w-7xl items-center px-6 py-16">

        <div className="grid w-full items-center gap-16 lg:grid-cols-2">

          {/* Left Section */}
          <div>

            <span className="inline-block rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
              🚀 AI Powered Career Assistant
            </span>

            <h1 className="mt-6 text-5xl font-extrabold leading-tight text-gray-900 lg:text-7xl">
              Land Your
              <span className="block text-blue-600">
                Dream Job
              </span>
              with AI
            </h1>

            <p className="mt-6 max-w-xl text-lg leading-8 text-gray-600">
              Analyze your resume, improve ATS score,
              practice AI interviews, and receive
              personalized career feedback—all in one platform.
            </p>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row">

              <Link
                to="/resume"
                className="rounded-xl bg-blue-600 px-8 py-4 text-center font-semibold text-white transition duration-300 hover:scale-105 hover:bg-blue-700"
              >
                Analyze Resume
              </Link>

              <Link
                to="/interview"
                className="rounded-xl border border-gray-300 bg-white px-8 py-4 text-center font-semibold text-gray-700 transition duration-300 hover:scale-105 hover:border-blue-600 hover:text-blue-600"
              >
                Start Interview
              </Link>

            </div>

          </div>

          {/* Right Section */}

          <Card className="overflow-hidden p-8">

  <div className="space-y-6">

    {/* Title */}

    <div className="flex items-center justify-between">

      <div>

        <h2 className="text-2xl font-bold">
          AI Analysis
        </h2>

        <p className="text-sm text-gray-500">
          Powered by FastAPI + LangChain + Groq
        </p>

      </div>

      <span className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
        LIVE
      </span>

    </div>

    {/* Workflow */}

    <div className="space-y-4">

      <div className="flex items-center gap-4 rounded-xl bg-gray-50 p-4">

        <span className="text-2xl">
          📄
        </span>

        <div>

          <h3 className="font-semibold">
            Resume.pdf
          </h3>

          <p className="text-sm text-gray-500">
            Uploaded Successfully
          </p>

        </div>

      </div>

      <div className="flex justify-center text-3xl text-blue-500">
        ↓
      </div>

      <div className="rounded-xl bg-blue-50 p-4">

        🤖 Extracting Resume Text...

      </div>

      <div className="flex justify-center text-3xl text-blue-500">
        ↓
      </div>

      <div className="rounded-xl bg-purple-50 p-4">

        🧠 Matching Resume with Job Description...

      </div>

      <div className="flex justify-center text-3xl text-blue-500">
        ↓
      </div>

      <div className="rounded-xl bg-yellow-50 p-4">

        ⚡ Generating ATS Report...

      </div>

      <div className="flex justify-center text-3xl text-blue-500">
        ↓
      </div>

    </div>

    {/* Result */}

    <div className="rounded-2xl border border-green-200 bg-green-50 p-6">

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-lg font-semibold">
            ATS Score
          </h2>

          <p className="text-sm text-gray-600">
            Resume Successfully Analyzed
          </p>

        </div>

        <span className="text-5xl font-extrabold text-green-600">
          92%
        </span>

      </div>

      <div className="mt-5 h-3 rounded-full bg-green-200">

        <div
          className="h-3 rounded-full bg-green-600"
          style={{ width: "92%" }}
        />

      </div>

    </div>

  </div>

</Card>

        </div>

      </div>
    </section>
  );
};

export default Hero;