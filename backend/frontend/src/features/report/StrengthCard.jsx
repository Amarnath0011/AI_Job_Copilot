const StrengthCard = ({ strengths }) => {
    return (
      <div className="rounded-2xl bg-white p-8 shadow-lg">
  
        <h2 className="mb-6 text-2xl font-bold text-green-600">
          Strengths
        </h2>
  
        <ul className="space-y-4">
  
          {strengths.map((item) => (
            <li
              key={item}
              className="rounded-xl bg-green-50 p-4"
            >
              ✅ {item}
            </li>
          ))}
  
        </ul>
  
      </div>
    );
  };
  
  export default StrengthCard;