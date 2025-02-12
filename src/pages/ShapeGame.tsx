import React from 'react';

export function ShapeGame() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
        <h1 className="text-3xl font-bold text-center mb-8">Shape Detection Game</h1>
        <p className="text-gray-600 text-center mb-8">
          Python integration coming soon! This game will test your pattern recognition abilities.
        </p>
        <div className="bg-gray-100 rounded-lg p-12 flex items-center justify-center">
          <p className="text-xl text-gray-500">Game content will be integrated here</p>
        </div>
      </div>
    </div>
  );
}