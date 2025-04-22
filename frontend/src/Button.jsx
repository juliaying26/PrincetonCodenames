export default function Button({ type, onClick, className, children }) {
  return (
    <button
      className={`${className}
        ${
          type == 'primary'
            ? 'bg-orange-500 rounded-md px-2 cursor-pointer font-medium hover:bg-orange-400'
            : 'bg-orange-50 rounded-md px-2 cursor-pointer font-medium hover:bg-orange-100'
        }`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
