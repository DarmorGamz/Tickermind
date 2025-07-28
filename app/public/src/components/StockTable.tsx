import React from 'react';
import { Stock, Column } from '../types';
import { formatCurrency, formatPercent, formatVolume, formatMarketCap } from '../utils/formatters';

interface StockTableProps {
  stocks: Stock[];
  visibleColumns: Column[];
}

const StockTable: React.FC<StockTableProps> = ({ stocks, visibleColumns }) => {
  const renderCellContent = (stock: Stock, columnId: Column) => {
    switch (columnId) {
      case 'symbol':
        return (
          <div className="flex flex-col">
            <span className="font-medium">{stock.symbol}</span>
            <span className="text-xs text-gray-400">{stock.name}</span>
          </div>
        );
      case 'price':
        return formatCurrency(stock.price);
      case 'changePercent': {
        const isPositive = stock.changePercent >= 0;
        return (
          <span className={`${isPositive ? 'text-green-400' : 'text-red-400'}`}>
            {formatPercent(stock.changePercent)}
          </span>
        );
      }
      case 'volume':
        return stock.volume ? formatVolume(stock.volume) : 'N/A';
      case 'marketCap':
        return stock.marketCap ? formatMarketCap(stock.marketCap) : 'N/A';
      case 'peRatio':
        return stock.peRatio ? stock.peRatio.toFixed(1) : 'N/A';
      default:
        return 'N/A';
    }
  };

  const getColumnLabel = (columnId: Column): string => {
    switch (columnId) {
      case 'symbol': return 'Symbol';
      case 'price': return 'Price';
      case 'changePercent': return 'Change %';
      case 'volume': return 'Volume';
      case 'marketCap': return 'Market Cap';
      case 'peRatio': return 'P/E Ratio';
      default: return columnId;
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
        <thead>
          <tr className="bg-gray-850 border-b border-gray-700">
            {visibleColumns.map((columnId) => (
              <th 
                key={columnId} 
                className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
              >
                {getColumnLabel(columnId)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {stocks.map((stock, index) => (
            <tr 
              key={stock.symbol} 
              className={`${index % 2 === 0 ? 'bg-gray-800' : 'bg-gray-850'} hover:bg-gray-700 transition-colors duration-150`}
            >
              {visibleColumns.map((columnId) => (
                <td key={`${stock.symbol}-${columnId}`} className="px-4 py-3 text-sm text-gray-200">
                  {renderCellContent(stock, columnId)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;