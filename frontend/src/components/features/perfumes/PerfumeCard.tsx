import React, { useState } from 'react';
import type { Perfume } from '../../../types';
import { Button } from '../../common/Button';
import { useCart } from '../../../contexts/CartContext';

interface PerfumeCardProps {
  perfume: Perfume;
  onViewDetails: (perfume: Perfume) => void;
}

export const PerfumeCard: React.FC<PerfumeCardProps> = ({ 
  perfume, 
  onViewDetails 
}) => {
  const [isAdding, setIsAdding] = useState(false);
  const { addToCart } = useCart();
  const handleAddToCart = async () => {
    try {
      setIsAdding(true);
      await addToCart(perfume);
    } catch (error) {
      console.error('Failed to add to cart:', error);
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full">
      <div 
        className="h-48 bg-gray-200 cursor-pointer flex-shrink-0"
        onClick={() => onViewDetails(perfume)}
      >
        <img
          key={perfume.id}
          src={perfume.img_url || '/src/images/placeholder.jpg'}
          alt={perfume.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            if (target.src !== '/src/images/placeholder.jpg' && target.src !== window.location.origin + '/src/images/placeholder.jpg') {
              target.src = '/src/images/placeholder.jpg';
            }
          }}
        />
      </div>
      
      <div className="p-4 flex flex-col flex-1">
        <h3 
          className="font-semibold text-lg mb-2 cursor-pointer hover:text-blue-600 line-clamp-2"
          onClick={() => onViewDetails(perfume)}
        >
          {perfume.name}
        </h3>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-1 flex-shrink-0">
          {perfume.description || 'Описание отсутствует'}
        </p>
        
        <div className="flex items-center justify-between mb-3 flex-shrink-0">
          <span className="text-2xl font-bold text-green-600">
            {perfume.price.toLocaleString()} ₽
          </span>
          
          {perfume.stock_quantity > 0 ? (
            <span className="text-sm text-green-600 bg-green-100 px-2 py-1 rounded whitespace-nowrap">
              В наличии
            </span>
          ) : (
            <span className="text-sm text-red-600 bg-red-100 px-2 py-1 rounded whitespace-nowrap">
              Нет в наличии
            </span>
          )}
        </div>
        
        <div className="flex gap-2 mt-auto flex-shrink-0">
          <Button
            variant="primary"
            size="sm"
            className="flex-1"
            loading={isAdding}
            disabled={perfume.stock_quantity === 0}
            onClick={handleAddToCart}
          >
            В корзину
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => onViewDetails(perfume)}
          >
            Подробнее
          </Button>
        </div>
      </div>
    </div>
  );
};