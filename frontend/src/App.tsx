import React, { useState, useEffect, useMemo } from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import SearchFilters from './components/SearchFilters';
import StockTable from './components/StockTable';
import { Stock, ColumnConfig, Column } from './types';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './components/theme-provider';
import LoginForm from './components/Auth/LoginForm';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';

function App() {

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <AuthProvider>
        <Router>
          <div className='min-h-screen bg-gray-50'>
            <Routes>
              <Route path='/login' element={<LoginForm />} />
              <Route
                path='/*'
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Navigate to='/dashboard' replace />} />
                <Route path ='dashboard' element={<Dashboard />} />
              </Route>
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;