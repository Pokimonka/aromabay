import React, { useState } from 'react';
import type { Perfume } from '../types';
import { PerfumeCard }from '../components/features/perfumes/PerfumeCard' 
import { PerfumeFilters } from '../components/features/perfumes/PerfumeFilters';
import { usePerfumes } from '../hooks/usePerfumes';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

interface CatalogProps {
  onViewProduct: (perfume: Perfume) => void;
}

export const Catalog: React.FC<CatalogProps> = ({ onViewProduct }) => {
  const [filters, setFilters] = useState({
    search: '',
    sort: 'name',
  });

  const { perfumes, loading, error } = usePerfumes(filters);

  const handleSearch = (search: string) => {
    setFilters(prev => ({ ...prev, search }));
  };

  const handleSort = (sort: string) => {
    setFilters(prev => ({ ...prev, sort }));
  };

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-red-600">
          <p>Ошибка загрузки каталога: {error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
          >
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Каталог духов</h1>
        <p className="text-gray-600">Найдите свой идеальный аромат</p>
      </div>

      <PerfumeFilters
        search={filters.search}
        sort={filters.sort}
        onSearchChange={handleSearch}
        onSortChange={handleSort}
      />

      {loading ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : (
        <>
          <div className="mb-4 text-gray-600">
            Найдено {perfumes.length} товаров
          </div>

          {perfumes.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">Товары не найдены</p>
              <p className="text-gray-400">Попробуйте изменить параметры поиска</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {perfumes.map(perfume => (
                <PerfumeCard
                  key={perfume.id}
                  perfume={perfume}
                  onViewDetails={onViewProduct}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};