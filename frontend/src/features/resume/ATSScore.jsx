const ATSScore = ({ data }) => {
    if (!data) return <h2>No ATS Analysis</h2>;
  
    return (
      <div>
        <h2>ATS Score</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  };
  
  export default ATSScore;