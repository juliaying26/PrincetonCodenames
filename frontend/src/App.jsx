import { useState, useEffect } from 'react';

function App() {
  const [gameBoard, setGameBoard] = useState([]);

  const getNewBoard = () => {
    fetch('/api/getboard')
      .then((response) => response.json())
      .then((data) => {
        setGameBoard(data);
      })
      .catch((error) => {
        console.error('Error fetching new board:', error);
      });
  };

  useEffect(() => {
    getNewBoard();
  }, []);

  useEffect(() => {
    console.log('Updated board:', gameBoard);
  }, [gameBoard]);

  return (
    <>
      <div className="flex justify-center gap-20 items-center h-screen bg-zinc-300">
        <div className="flex flex-col gap-5 items-center justify-center text-center">
          {gameBoard.map((row, rowIndex) => (
            <div className="flex gap-5 items-center justify-center" key={rowIndex}>
              {row.map(([word, color], colIndex) => (
                <div
                  key={colIndex}
                  className="rounded-xl flex w-50 h-28 border border-gray-300 p-2 items-center justify-center text-xl font-semibold"
                  style={{
                    backgroundColor: color,
                  }}
                >
                  {word}
                </div>
              ))}
            </div>
          ))}
        </div>
        <div>
          <button className="bg-blue-500">Guess</button>
        </div>
      </div>
    </>
  );
}

export default App;
