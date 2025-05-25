import React, { useState, useMemo } from 'react';
import Navbar from './components/Navbar';

import SearchFilters from './components/SearchFilters';
import StockTable from './components/StockTable';
import { stockData, columns } from './data/stocks';
import { Column } from './types';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [visibleColumns, setVisibleColumns] = useState<Column[]>(
    columns.filter(col => !col.optional).map(col => col.id)
  );

  // Filter stocks based on search term
  const filteredStocks = useMemo(() => {
    if (!searchTerm.trim()) return stockData;
    
    const searchLower = searchTerm.toLowerCase();
    return stockData.filter(stock => 
      stock.symbol.toLowerCase().includes(searchLower) || 
      stock.name.toLowerCase().includes(searchLower)
    );
  }, [searchTerm]);

  // Toggle column visibility
  const toggleColumn = (columnId: string) => {
    setVisibleColumns(prevColumns => {
      if (prevColumns.includes(columnId as Column)) {
        return prevColumns.filter(col => col !== columnId);
      } else {
        return [...prevColumns, columnId as Column];
      }
    });
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <Navbar />
      
      <main className="container mx-auto px-4 py-6 max-w-full">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Stock Screener</h1>
          <p>Find and analyze stocks with our powerful screening tool</p>
        </div>

        <SearchFilters 
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          columns={columns}
          visibleColumns={visibleColumns}
          toggleColumn={toggleColumn}
        />
        
        {filteredStocks.length > 0 ? (
          <StockTable 
            stocks={filteredStocks} 
            visibleColumns={visibleColumns}
          />
        ) : (
          <div className="bg-gray-800 rounded-lg p-8 text-center border border-gray-700">
            <p className="text-gray-300">No stocks found matching "{searchTerm}"</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;