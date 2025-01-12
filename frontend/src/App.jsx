import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

const socket = io("http://127.0.0.1:8000");

function App() {
  const [gameState, setGameState] = useState({
    paddles: { player1: 50, player2: 50 },
    ball: { x: 50, y: 50 },
    scores: { player1: 0, player2: 0 },
    obstacles: [], // Ensure obstacles are initialized as an empty array
  });

  const [player, setPlayer] = useState(null); // Assigned player (player1 or player2)

  // Handle incoming game state updates
  useEffect(() => {
    socket.on("update_game", (state) => {
      setGameState(state);
    });

    socket.on("assign_player", (data) => {
      setPlayer(data.player); // Assign player1 or player2
      console.log(`You are ${data.player}`);
    });

    socket.on("game_full", () => {
      alert("Game is full! Please wait for a spot.");
    });

    return () => {
      socket.off("update_game");
      socket.off("assign_player");
      socket.off("game_full");
    };
  }, []);

  // Handle keyboard events for paddle movement
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (!player) return; // Do nothing if player role is not assigned

      const step = 5; // Amount to move the paddle with each key press
      let newPosition = gameState.paddles[player];

      if (event.key === "ArrowUp") {
        newPosition = Math.max(0, gameState.paddles[player] - step); // Move up
      } else if (event.key === "ArrowDown") {
        newPosition = Math.min(100, gameState.paddles[player] + step); // Move down
      }

      // Emit paddle movement to the backend
      if (newPosition !== gameState.paddles[player]) {
        socket.emit("move_paddle", { player, position: newPosition });
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [gameState, player]);

  // Restart the game
  const restartGame = () => {
    socket.emit("restart_game");
  };

  return (
    <div className="App">
      <div className="game-board">
        <div
          className="paddle player1"
          style={{ top: `${gameState.paddles.player1}%` }}
        ></div>
        <div
          className="paddle player2"
          style={{ top: `${gameState.paddles.player2}%` }}
        ></div>
        <div
          className="ball"
          style={{
            left: `${gameState.ball.x}%`,
            top: `${gameState.ball.y}%`,
          }}
        ></div>
        {/* Render obstacles only if they exist */}
        {gameState.obstacles?.map((obstacle, index) => (
          <div
            key={index}
            className="obstacle"
            style={{
              left: `${obstacle.x}%`,
              top: `${obstacle.y}%`,
              width: `${obstacle.size}%`,
              height: `${obstacle.size + 5}%`,
            }}
          ></div>
        ))}
        <div className="scoreboard">
          Player 1: {gameState.scores.player1} | Player 2: {gameState.scores.player2}
        </div>
      </div>
      <div className="controls">
        <p>{player ? `You are ${player}` : "Waiting for role assignment..."}</p>
        <p>Use Arrow Keys to move the paddle.</p>
        <button onClick={restartGame} className="restart-button">
          Restart Game
        </button>
      </div>
    </div>
  );
  
}

export default App;
