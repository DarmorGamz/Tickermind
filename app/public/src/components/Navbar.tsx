import React from 'react';
import { ChartCandlestick, User, LogOut, Menu } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { logout } = useAuth();
  const location = useLocation();
  const { user } = useAuth();

  return (
    <nav className="bg-[#181818] px-4 py-3 flex justify-between items-center">
      <div className="flex items-center space-x-2 cursor-pointer" onClick={() => window.location.reload()}>
        <ChartCandlestick className="h-6 w-6" />
        <span className="text-white font-bold text-xl">TickerMind</span>
      </div>

      <div className="relative flex items-center space-x-2">
        <div className='flex items-center space-x-2 p-2 cursor-pointer rounded-2xl border-2 border-[#181818] hover:border-blue-500 hover:bg-blue-950 transition-colors duration-300'>
          <div className="h-8 w-8 rounded-full hover:border-blue-500 bg-gray-700 flex items-center justify-center overflow-hidden ">
            <User className="h-5 w-5 text-gray-300" />
          </div>
          <span className="truncate max-w-24 md:max-w-none">{user?.email}</span>
        </div>
        <button
            onClick={logout}
            className="p-2 rounded-md text-gray-400 hover:text-red-600 hover:bg-red-300 transition-colors touch-manipulation"
            title="Logout"
          >
            <LogOut size={16} />
          </button>
      </div>
    </nav>
  );
};

export default Navbar;