const ResumeFeedback = ({ data }) => {
    if (!data) return <h2>No Feedback</h2>;
  
    return (
      <div>
        <h2>Resume Feedback</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  };
  
  export default ResumeFeedback;