import React, { useState, useMemo } from 'react';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navbar />
      
      <main className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Stock Screener</h1>
          <p>Find and analyze stocks with our powerful screening tool</p>
        </div>
      </main>
    </div>
  );
}

export default App;