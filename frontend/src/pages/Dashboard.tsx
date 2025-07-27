import React, { useState, useEffect, useMemo } from 'react';
import Navbar from '../components/Navbar';

import SearchFilters from '../components/SearchFilters';
import StockTable from '../components/StockTable';
import { Stock, ColumnConfig, Column } from '../types';

const Dashboard: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [visibleColumns, setVisibleColumns] = useState<Column[]>([]);
  const [columns, setColumns] = useState<ColumnConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch columns (one-time) and stocks (initial fetch + polling)
  useEffect(() => {
    const fetchColumns = async () => {
      try {
        const columnsResponse = await fetch('http://localhost:8000/api/columns');
        if (!columnsResponse.ok) {
          throw new Error('Failed to fetch columns');
        }
        const columnsData: ColumnConfig[] = await columnsResponse.json();
        setColumns(columnsData);
        setVisibleColumns(
          columnsData.filter(col => !col.optional).map(col => col.id)
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    const fetchStocks = async () => {
      try {
        const stocksResponse = await fetch('http://localhost:8000/api/stocks');
        if (!stocksResponse.ok) {
          throw new Error('Failed to fetch stocks');
        }
        const stocksData: Stock[] = await stocksResponse.json();
        setStocks(stocksData);
        setError(null); // Clear error on success
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    const initializeData = async () => {
      setLoading(true);
      await Promise.all([fetchColumns(), fetchStocks()]);
      setLoading(false);
    };

    initializeData();

    // Polling for stocks every second
    const intervalId = setInterval(fetchStocks, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);
  
  // Filter stocks based on search term
  const filteredStocks = useMemo(() => {
    if (!searchTerm.trim()) return stocks;

    const searchLower = searchTerm.toLowerCase();
    return stocks.filter(
      stock =>
        stock.symbol.toLowerCase().includes(searchLower) ||
        stock.name.toLowerCase().includes(searchLower)
    );
  }, [searchTerm, stocks]);

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
    <main className="container mx-auto px-4 py-6 max-w-full">
        <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">Stock Screener</h1>
        <p>Find and analyze stocks with our powerful screening tool</p>
        </div>

        {loading ? (
        <div className="bg-gray-800 rounded-lg p-8 text-center border border-gray-700">
            <p className="text-gray-300">Loading...</p>
        </div>
        ) : error ? (
        <div className="bg-red-900 rounded-lg p-8 text-center border border-red-700">
            <p className="text-red-300">Error: {error}</p>
        </div>
        ) : (
        <>
            <SearchFilters
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            columns={columns}
            visibleColumns={visibleColumns}
            toggleColumn={toggleColumn}
            />
            {filteredStocks.length > 0 ? (
            <StockTable stocks={filteredStocks} visibleColumns={visibleColumns} />
            ) : (
            <div className="bg-gray-800 rounded-lg p-8 text-center border border-gray-700">
                <p className="text-gray-300">No stocks found matching "{searchTerm}"</p>
            </div>
            )}
        </>
        )}
    </main>
    </div>
  );
};

export default Dashboard;