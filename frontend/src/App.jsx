import { useState, useEffect } from 'react';
import Dropdown from './Dropdown.jsx';
import Button from './Button.jsx';

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
  const [roundNumber, setRoundNumber] = useState(1);
  const [previousBoard, setPreviousBoard] = useState([]);
  const [flippingTiles, setFlippingTiles] = useState([]);

  const getNewBoard = () => {
    fetch(`${import.meta.env.VITE_API_URL}/api/getboard`)
      .then((response) => response.json())
      .then((data) => {
        setGameBoard(data);
      })
      .catch((error) => {
        console.error('Error fetching new board:', error);
      });
  };

  const getDropdownWords = () => {
    fetch(`${import.meta.env.VITE_API_URL}/api/getdropdownoptions`)
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

    fetch(`${import.meta.env.VITE_API_URL}/api/guessword`, {
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
    fetch(`${import.meta.env.VITE_API_URL}/api/opponentplay`, {
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
    fetch(`${import.meta.env.VITE_API_URL}/api/resetgame`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then(() => {
        setPreviousBoard([]);
        getNewBoard();
        getDropdownWords();
        setGuessNumber(1);
        setGuessMessage('');
        setSelectedWord([]);
        getClue();
        setOpponentClue([]);
        setOpponentPlaying(false);
        setWinner('');
        setRoundNumber(1);
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
    setRoundNumber((prev) => prev + 1);
    getClue();
  };

  const handleSkipGuess = () => {
    setSelectedWord([]);
    setGuessNumber(1);
    setGuessMessage('');
    setOpponentPlaying(true);
  };

  const getClue = () => {
    fetch(`${import.meta.env.VITE_API_URL}/api/getclue`)
      .then((response) => response.json())
      .then((data) => {
        setClue([data.clue, data.clue_size]);
      })
      .catch((error) => {
        console.error('Error fetching clue:', error);
      });
  };

  const getScore = () => {
    fetch(`${import.meta.env.VITE_API_URL}/api/getscore`)
      .then((response) => response.json())
      .then((data) => {
        setScore({ player: data.player_score, opponent: data.opponent_score });
      })
      .catch((error) => {
        console.error('Error fetching score:', error);
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
      setWinner('COMPUTER');
    }
    if (guessMessage.includes('turn is over')) {
      setOpponentPlaying(true);
    }
  }, [guessMessage]);

  useEffect(() => {
    if (opponentClue[2]?.includes('assassin')) {
      setWinner('YOU');
    }
  }, [opponentClue]);

  useEffect(() => {
    getScore();
  }, [gameBoard]);

  useEffect(() => {
    if (previousBoard.length === 0) {
      setPreviousBoard(gameBoard);
      return;
    }

    const flips = gameBoard.flat().map(([word, color], index) => {
      const [_, prevColor] = previousBoard.flat()[index] || [];
      return color !== prevColor;
    });

    setFlippingTiles(flips);
    setPreviousBoard(gameBoard);

    const timeout = setTimeout(() => {
      setFlippingTiles(gameBoard.flat().map(() => false));
    }, 500); // match animation duration

    return () => clearTimeout(timeout);
  }, [gameBoard]);

  useEffect(() => {
    if (score.player == 9) {
      setWinner('YOU');
    }
    if (score.opponent == 8) {
      setWinner('COMPUTER');
    }
  }, [score]);

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
                {row.map(([word, color], colIndex) => {
                  const index = rowIndex * 5 + colIndex;
                  const isFlipping = flippingTiles[index];

                  return (
                    <div
                      key={colIndex}
                      className={`transition-transform duration-500 transform ${
                        isFlipping ? 'rotate-x-180' : ''
                      }`}
                    >
                      <div
                        className="rounded-xl flex w-50 h-28 border border-[#DBBE6A] p-2 items-center justify-center text-xl font-semibold"
                        style={{
                          backgroundColor: color,
                        }}
                      >
                        <div className="flex rounded-xl bg-white py-3 w-44 items-center justify-center">
                          {word}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
          <div className="flex flex-col gap-4">
            <div className="text-2xl font-bold w-64">Round {roundNumber}</div>
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
                  <Button
                    className="ml-auto border-orange-500  py-1"
                    type="secondary"
                    onClick={handleSkipGuess}
                  >
                    Skip guess
                  </Button>
                </div>
                <Dropdown
                  options={dropdownWords}
                  selected={selectedWord}
                  setSelected={setSelectedWord}
                />
                <Button type="primary" className="w-64 py-2" onClick={handleGuessWord}>
                  Guess Word!
                </Button>
              </div>
            )}
            {opponentClue.length !== 0 && (
              <div className="flex flex-col gap-2 w-64">
                {!winner && (
                  <p className="text-2xl font-semibold">
                    Opponent Clue: {opponentClue[0]?.toUpperCase()}, {opponentClue[1]}
                  </p>
                )}
                {opponentClue[2].split('\n').map((line, idx) => (
                  <p className="text-md font-medium w-64" key={idx}>
                    {line}
                  </p>
                ))}
                {!winner && (
                  <Button type="secondary" className="w-64 py-2" onClick={handleMyTurn}>
                    Back to your turn
                  </Button>
                )}
              </div>
            )}
            {opponentClue.length == 0 && (
              <p className="text-md font-medium w-64">
                {guessMessage && 'Guess ' + (guessNumber - 1) + ': ' + guessMessage}
              </p>
            )}
            {!winner && opponentPlaying && (
              <Button type="secondary" className="w-64 py-2" onClick={handleOpponentPlay}>
                Let computer play
              </Button>
            )}
            {winner && (
              <div className="text-xl font-semibold w-64">
                {'🏆 ' + winner} {winner == 'COMPUTER' ? 'WINS!' : 'WIN!'}
              </div>
            )}
            {
              <Button type="primary" className="w-64 py-2" onClick={resetGame}>
                Restart Game
              </Button>
            }
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
