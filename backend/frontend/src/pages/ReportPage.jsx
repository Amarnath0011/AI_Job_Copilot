import { useLocation, Navigate } from "react-router-dom";
import FinalReport from "../features/report/FinalReport";

const ReportPage = () => {
  const { state } = useLocation();

  if (!state?.report) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="mx-auto max-w-7xl px-6">
        <FinalReport report={state.report} />
      </div>
    </div>
  );
};

export default ReportPage;