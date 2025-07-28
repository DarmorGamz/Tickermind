import React from 'react';
import { Search } from 'lucide-react';
import { ColumnConfig } from '../types';

interface SearchFiltersProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  columns: ColumnConfig[];
  visibleColumns: string[];
  toggleColumn: (columnId: string) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({
  searchTerm,
  setSearchTerm,
  columns,
  visibleColumns,
  toggleColumn
}) => {
  return (
    <div className="bg-gray-850 p-4 rounded-lg mb-4 border border-gray-700 space-y-4">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          className="block w-full pl-10 pr-3 py-2 border border-gray-600 rounded-md leading-5 bg-gray-800 text-gray-200 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out sm:text-sm"
          placeholder="Search by symbol or name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      
      <div>
        <div className="flex flex-wrap gap-3">
          {columns.map(column => (
            column.optional && (
              <label 
                key={column.id}
                className="inline-flex items-center cursor-pointer"
              >
                <input
                  type="checkbox"
                  className="form-checkbox rounded bg-gray-700 border-gray-600 text-blue-500 focus:ring-blue-500 focus:ring-opacity-50"
                  checked={visibleColumns.includes(column.id)}
                  onChange={() => toggleColumn(column.id)}
                />
                <span className="ml-2 text-sm text-gray-300">{column.label}</span>
              </label>
            )
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchFilters;