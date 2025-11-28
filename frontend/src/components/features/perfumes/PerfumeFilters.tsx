import React from 'react';
import { Input } from '../../common/Input';

interface PerfumeFiltersProps {
  search: string;
  sort: string;
  onSearchChange: (search: string) => void;
  onSortChange: (sort: string) => void;
}

export const PerfumeFilters: React.FC<PerfumeFiltersProps> = ({
  search,
  sort,
  onSearchChange,
  onSortChange,
}) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border mb-6">
      <div className="flex flex-col md:flex-row gap-4">
        {/* Поиск */}
        <div className="flex-1">
          <Input
            type="text"
            placeholder="Поиск по названию или описанию..."
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full"
          />
        </div>
        
        {/* Сортировка */}
        <div className="w-full md:w-48">
          <select
            value={sort}
            onChange={(e) => onSortChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="name">По названию</option>
            <option value="price_asc">Цена по возрастанию</option>
            <option value="price_desc">Цена по убыванию</option>
            <option value="newest">Сначала новые</option>
          </select>
        </div>
      </div>
    </div>
  );
};