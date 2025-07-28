import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

const Layout: React.FC = () => {;

  return (
    <div className="h-screen bg-black flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;