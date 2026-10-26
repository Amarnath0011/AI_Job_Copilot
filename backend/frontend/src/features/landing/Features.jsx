import Card from "../../components/ui/Card";

const features = [
  {
    icon: "📝",
    title: "Resume Analysis",
    description:
      "Upload your resume and receive detailed AI-powered ATS analysis with personalized feedback.",
  },
  {
    icon: "🎯",
    title: "ATS Optimization",
    description:
      "Compare your resume with any Job Description and identify missing keywords instantly.",
  },
  {
    icon: "🎤",
    title: "AI Mock Interview",
    description:
      "Practice adaptive technical interviews with AI-generated questions and instant evaluation.",
  },
  {
    icon: "📊",
    title: "Performance Report",
    description:
      "Receive detailed interview reports with strengths, weaknesses and improvement suggestions.",
  },
];

const Features = () => {
  return (
    <section className="bg-gray-50 py-24">
      <div className="mx-auto max-w-7xl px-6">

        {/* Heading */}

        <div className="mb-16 text-center">

          <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-600">
            FEATURES
          </span>

          <h2 className="mt-5 text-4xl font-bold text-gray-900 md:text-5xl">
            Why Choose AI Job Copilot?
          </h2>

          <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-gray-600">
            Everything you need to build a stronger resume,
            prepare for technical interviews, and land your dream job.
          </p>

        </div>

        {/* Cards */}

        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">

          {features.map((feature) => (

            <Card
              key={feature.title}
              className="group cursor-pointer text-center"
            >

              <div className="mb-6 text-6xl transition-transform duration-300 group-hover:scale-110">
                {feature.icon}
              </div>

              <h3 className="mb-4 text-2xl font-bold text-gray-900">
                {feature.title}
              </h3>

              <p className="leading-7 text-gray-600">
                {feature.description}
              </p>

            </Card>

          ))}

        </div>

      </div>
    </section>
  );
};

export default Features;