import React, { useState, useRef, useEffect } from 'react';
import { ChartCandlestick, User } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-black px-4 py-3 flex justify-between items-center">
      <div className="flex items-center space-x-2 cursor-pointer" onClick={() => window.location.reload()}>
        <ChartCandlestick className="h-6 w-6" />
        <span className="text-white font-bold text-xl">TickerMind</span>
      </div>
      
      <div className="relative">
        <div className="h-10 w-10 rounded-full bg-gray-700 flex items-center justify-center cursor-pointer overflow-hidden border-2 border-gray-600 hover:border-blue-500 transition-colors duration-300">
          <User className="h-6 w-6 text-gray-300" />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;