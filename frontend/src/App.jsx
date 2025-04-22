import { useState, useEffect } from 'react';
import Dropdown from './Dropdown.jsx';

function App() {
  const [gameBoard, setGameBoard] = useState([]);
  const [dropdownWords, setDropdownWords] = useState([]);
  const [selectedWord, setSelectedWord] = useState([]);
  const [clue, setClue] = useState([]);
  const [opponentClue, setOpponentClue] = useState([]);
  const [guessNumber, setGuessNumber] = useState(1);
  const [guessMessage, setGuessMessage] = useState('');
  const [opponentPlaying, setOpponentPlaying] = useState(false);
  const [score, setScore] = useState({ player: 0, opponent: 0 });
  const [winner, setWinner] = useState('');

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
      body: JSON.stringify({
        word: selectedWord[0].value,
        guess_number: guessNumber,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setGuessMessage(data.message);
        setSelectedWord([]);
        getNewBoard();
        setGuessNumber((prev) => prev + 1);
        getDropdownWords();
      })
      .catch((error) => {
        console.error('Error guessing word:', error);
      });
  };

  const handleOpponentPlay = () => {
    fetch('/api/opponentplay', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setOpponentClue([data.clue, data.clue_size, data.message]);
        setOpponentPlaying(false);
        setSelectedWord([]);
        setGuessNumber(1);
        getNewBoard();
        setGuessNumber((prev) => prev + 1);
        getDropdownWords();
      })
      .catch((error) => {
        console.error('Error letting opponent play:', error);
      });
  };

  const resetGame = () => {
    fetch('/api/resetgame', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then(() => {
        getNewBoard();
        getDropdownWords();
        setGuessNumber(1);
        setGuessMessage('');
        setSelectedWord([]);
        getClue();
        setOpponentClue([]);
        setOpponentPlaying(false);
        setWinner('');
      })
      .catch((error) => {
        console.error('Error resetting game:', error);
      });
  };

  const handleMyTurn = () => {
    setOpponentClue([]);
    setOpponentPlaying(false);
    setGuessNumber(1);
    setGuessMessage('');
    setSelectedWord([]);
    getDropdownWords();
    getClue();
  };

  const handleSkipGuess = () => {
    setSelectedWord([]);
    setGuessNumber(1);
    setGuessMessage('');
    setOpponentPlaying(true);
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

  const getScore = () => {
    fetch('/api/getscore')
      .then((response) => response.json())
      .then((data) => {
        setScore({ player: data.player_score, opponent: data.opponent_score });
      })
      .catch((error) => {
        console.error('Error fetching score:', error);
      });
  };

  const checkGameOver = () => {
    fetch('/api/gameover')
      .then((response) => response.json())
      .then((data) => {
        if (data.game_over) {
          setOpponentPlaying(false);
          setWinner(data.winner);
        }
      })
      .catch((error) => {
        console.error('Error checking game over:', error);
      });
  };

  useEffect(() => {
    getNewBoard();
    getDropdownWords();
    getClue();
  }, []);

  useEffect(() => {
    console.log(winner);
  }, [winner]);

  useEffect(() => {
    if (guessMessage.includes('assassin')) {
      setWinner('You');
    } else if (opponentClue[2]?.includes('assassin')) {
      setWinner('Opponent');
    }
    if (guessMessage.includes('turn is over')) {
      setOpponentPlaying(true);
    }
  }, [guessMessage]);

  useEffect(() => {
    getScore();
    checkGameOver();
  }, [gameBoard]);

  return (
    <>
      <div className="flex flex-col h-screen bg-orange-300 items-center justify-center">
        <div className="pb-10 font-bold text-5xl">Princeton Codenames</div>
        <div className="absolute top-12 right-12 text-center">
          <p className="text-lg font-bold">Score</p>
          <p className="text-md font-semibold">
            You: {score.player} - Opponent: {score.opponent}
          </p>
        </div>
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
            {!winner && opponentClue.length == 0 && (
              <div className="text-2xl flex flex-col font-semibold gap-2 w-64">
                <p>
                  Your Clue: {clue[0]?.toUpperCase()}, {clue[1]}
                </p>
              </div>
            )}
            {!winner && !opponentPlaying && opponentClue.length == 0 && (
              <div className="flex flex-col gap-2 w-64">
                <div className="flex w-64 items-center">
                  <p className="text-xl">
                    Guess {guessNumber}/
                    {guessMessage.includes('extra guess') ? Number(clue[1]) + 1 : clue[1]}:
                  </p>
                  <button
                    className="ml-auto bg-white border-orange-500 border-2 rounded-md py-1 px-2 cursor-pointer font-medium"
                    onClick={handleSkipGuess}
                  >
                    Skip guess
                  </button>
                </div>
                <Dropdown
                  options={dropdownWords}
                  selected={selectedWord}
                  setSelected={setSelectedWord}
                />
                <button
                  className=" bg-orange-500 rounded-md py-2 px-2 cursor-pointer font-medium"
                  onClick={handleGuessWord}
                >
                  Guess Word!
                </button>
              </div>
            )}
            {!winner && opponentClue.length !== 0 && (
              <div className="flex flex-col gap-2 w-64">
                <p className="text-2xl font-semibold">
                  Opponent Clue: {opponentClue[0]?.toUpperCase()}, {opponentClue[1]}
                </p>
                {opponentClue[2].split('\n').map((line, idx) => (
                  <p className="text-md font-medium w-64" key={idx}>
                    {line}
                  </p>
                ))}
                <button
                  className="bg-white rounded-md py-2 px-2 cursor-pointer font-medium"
                  onClick={handleMyTurn}
                >
                  Back to your turn
                </button>
              </div>
            )}
            {opponentClue.length == 0 && (
              <p className="text-md font-medium w-64">
                {guessMessage && 'Guess ' + (guessNumber - 1) + ': ' + guessMessage}
              </p>
            )}
            {opponentPlaying && (
              <button
                className="w-64 bg-white rounded-md py-2 px-2 cursor-pointer font-medium"
                onClick={handleOpponentPlay}
              >
                Let computer play
              </button>
            )}
            {winner && (
              <div className="text-xl font-semibold w-64">
                {'🏆 ' + winner} {winner == 'COMPUTER' ? 'WINS!' : 'WIN!'}
              </div>
            )}
            {
              <button
                className="bg-orange-500 rounded-md py-2 px-2 cursor-pointer font-medium"
                onClick={resetGame}
              >
                Restart Game
              </button>
            }
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
