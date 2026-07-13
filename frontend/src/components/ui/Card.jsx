const Card = ({
    children,
    className = "",
  }) => {
    return (
      <div
        className={`
          rounded-2xl
          bg-white
          p-6
          shadow-lg
          border
          border-gray-100
          transition-all
          duration-300
          hover:-translate-y-1
          hover:shadow-xl
          ${className}
        `}
      >
        {children}
      </div>
    );
  };
  
  export default Card;