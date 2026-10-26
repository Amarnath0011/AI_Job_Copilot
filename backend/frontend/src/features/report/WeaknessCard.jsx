const WeaknessCard = ({ weaknesses }) => {
    return (
      <div className="rounded-2xl bg-white p-8 shadow-lg">
  
        <h2 className="mb-6 text-2xl font-bold text-red-600">
          Weaknesses
        </h2>
  
        <ul className="space-y-4">
  
          {weaknesses.map((item) => (
            <li
              key={item}
              className="rounded-xl bg-red-50 p-4"
            >
              ❌ {item}
            </li>
          ))}
  
        </ul>
  
      </div>
    );
  };
  
  export default WeaknessCard;