import React, { useState } from "react";

export function EmotionGame() {
  const [output, setOutput] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runEmotionGame = async () => {
    try {
      const response = await fetch("http://192.168.31.232:5000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script: "emotion_game.py" }),
      });

      const data = await response.json();
      setOutput(data.output || "Game started. Check the terminal.");
      setError(data.error || null);
    } catch (err) {
      setError("Failed to connect to server. Ensure Flask is running.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
        <h1 className="text-3xl font-bold text-center mb-8">
          Emotion Detection Game
        </h1>
        <p className="text-gray-600 text-center mb-8">
          Click the button to start the Emotion Detection game.
        </p>
        <div className="flex justify-center mb-6">
          <button
            onClick={runEmotionGame}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
          >
            Start Emotion Game
          </button>
        </div>
        <div className="bg-gray-100 rounded-lg p-4">
          {output && <p className="text-green-600">Output: {output}</p>}
          {error && <p className="text-red-600">Error: {error}</p>}
        </div>
      </div>
    </div>
  );
}
