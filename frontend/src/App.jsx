import { useState, useEffect } from 'react';
import Dropdown from './Dropdown.jsx';

function App() {
  const [gameBoard, setGameBoard] = useState([]);
  const [dropdownWords, setDropdownWords] = useState([]);
  const [selectedWord, setSelectedWord] = useState([]);
  const [clue, setClue] = useState([]);

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

  const getDropdownWords = () => {
    fetch('/api/getdropdownoptions')
      .then((response) => response.json())
      .then((data) => {
        setDropdownWords(data);
      })
      .catch((error) => {
        console.error('Error fetching dropdown words:', error);
      });
  };

  const handleGuessWord = () => {
    if (selectedWord.length === 0) {
      alert('Please select a word from the dropdown.');
      return;
    }

    fetch('/api/guessword', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word: selectedWord[0].value }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        setSelectedWord([]);
        getNewBoard();
        getDropdownWords();
      })
      .catch((error) => {
        console.error('Error guessing word:', error);
      });
  };

  const getClue = () => {
    fetch('/api/getclue')
      .then((response) => response.json())
      .then((data) => {
        setClue([data.clue, data.clue_size]);
      })
      .catch((error) => {
        console.error('Error fetching clue:', error);
      });
  };

  useEffect(() => {
    getNewBoard();
    getDropdownWords();
    getClue();
  }, []);

  useEffect(() => {
    console.log(clue);
  }, [clue]);

  return (
    <>
      <div className="flex flex-col h-screen bg-orange-300 items-center justify-center">
        <div className="pb-10 font-bold text-5xl">Princeton Codenames</div>
        <div className="flex justify-center gap-20 items-center">
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
                    <div className="flex rounded-xl bg-white py-3 w-44 items-center justify-center">
                      {word}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="flex flex-col gap-4">
            <div className="text-2xl flex flex-col font-semibold gap-2">
              <p>Clue: {clue[0]?.toUpperCase()}</p>
              <p>Number of Words: {clue[1]}</p>
            </div>
            Guess number: __
            <Dropdown
              options={dropdownWords}
              selected={selectedWord}
              setSelected={setSelectedWord}
            />
            <button
              className="bg-orange-500 rounded-md py-2 px-2 cursor-pointer"
              onClick={handleGuessWord}
            >
              Guess Word!
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
