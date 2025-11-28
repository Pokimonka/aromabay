import React, { useState } from 'react';
import type { Perfume } from '../types';
import { Button } from '../components/common/Button';
import { useCart } from '../contexts/CartContext';

interface ProductDetailProps {
  perfume: Perfume;
  onClose: () => void;
}

export const ProductDetail: React.FC<ProductDetailProps> = ({ 
  perfume, 
  onClose 
}) => {
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);
  const { addToCart } = useCart();

  // Проверяем, нужно ли показывать кнопку "Развернуть"
  // Показываем кнопку, если описание длиннее 150 символов или содержит более 3 строк
  const description = perfume.description || '';
  const shouldShowExpand = description.length > 150 || (description.split('\n').length > 3);

  const handleAddToCart = async () => {
    try {
      setIsAdding(true);
      for (let i = 0; i < quantity; i++) {
        await addToCart(perfume);
      }
      onClose();
    } catch (error) {
      console.error('Failed to add to cart:', error);
    } finally {
      setIsAdding(false);
    }
  };

  const increaseQuantity = () => {
    setQuantity(prev => prev + 1);
  };

  const decreaseQuantity = () => {
    setQuantity(prev => Math.max(1, prev - 1));
  };

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 overflow-y-auto overflow-x-hidden"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg max-w-4xl w-full my-8 shadow-xl overflow-hidden flex flex-col max-h-[90vh] mx-auto">
        <div className="flex flex-col lg:flex-row min-h-0 flex-1 overflow-hidden">
          {/* Изображение */}
          <div className="flex-1 p-4 lg:p-8 min-w-0 flex-shrink-0">
            <div className="bg-gray-100 rounded-lg h-64 sm:h-80 lg:h-96 flex items-center justify-center overflow-hidden">
              <img
                key={`${perfume.id}-${perfume.img_url || 'no-img'}`}
                src={perfume.img_url || '/src/images/placeholder.jpg'}
                alt={perfume.name}
                className="max-w-full max-h-full object-contain"
                loading="lazy"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  const placeholderPath = '/src/images/placeholder.jpg';
                  const currentSrc = target.src;
                  
                  // Предотвращаем бесконечный цикл ошибок
                  if (!currentSrc.includes('placeholder.jpg')) {
                    target.src = placeholderPath;
                    // Если и placeholder не загрузился, скрываем изображение
                    target.onerror = () => {
                      target.style.display = 'none';
                    };
                  }
                }}
              />
            </div>
          </div>

          {/* Информация */}
          <div className="flex-1 p-4 lg:p-8 lg:border-l border-t lg:border-t-0 min-w-0 overflow-y-auto">
            <div className="flex justify-between items-start mb-6 relative gap-2">
              <div className="flex-1 min-w-0 pr-2">
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2 break-words">
                  {perfume.name}
                </h2>
                <p className="text-gray-600 text-sm sm:text-base break-words">{perfume.brand}</p>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors flex-shrink-0"
                aria-label="Закрыть"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="mb-6">
              <span className="text-2xl sm:text-3xl font-bold text-green-600">
                {perfume.price.toLocaleString()} ₽
              </span>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold mb-2 text-gray-900">Описание</h3>
              <div className="relative w-full">
                <div 
                  className={`text-gray-700 leading-relaxed transition-all duration-300 w-full ${
                    shouldShowExpand && !isDescriptionExpanded 
                      ? 'max-h-24 overflow-hidden relative' 
                      : 'max-h-none'
                  }`}
                >
                  <p className="whitespace-pre-wrap break-words" style={{ wordBreak: 'break-word' }}>{description || 'Описание отсутствует'}</p>
                  {shouldShowExpand && !isDescriptionExpanded && (
                    <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-white to-transparent pointer-events-none"></div>
                  )}
                </div>
                
                {/* Кнопка "Развернуть/Свернуть" */}
                {shouldShowExpand && (
                  <button
                    onClick={() => setIsDescriptionExpanded(!isDescriptionExpanded)}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium mt-2 flex items-center gap-1 transition-colors w-full sm:w-auto"
                  >
                    <span>{isDescriptionExpanded ? 'Свернуть' : 'Развернуть'}</span>
                    <svg 
                      className={`w-4 h-4 transition-transform duration-200 flex-shrink-0 ${
                        isDescriptionExpanded ? 'rotate-180' : ''
                      }`} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="min-w-0">
                <span className="text-xs sm:text-sm text-gray-600 block mb-1">Концентрация</span>
                <p className="font-medium text-sm sm:text-base break-words">{perfume.concentration || 'Не указано'}</p>
              </div>
              <div className="min-w-0">
                <span className="text-xs sm:text-sm text-gray-600 block mb-1">Объем</span>
                <p className="font-medium text-sm sm:text-base break-words">{perfume.volume} мл</p>
              </div>
              <div className="min-w-0">
                <span className="text-xs sm:text-sm text-gray-600 block mb-1">Наличие</span>
                <p className={`font-medium text-sm sm:text-base break-words ${
                  perfume.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {perfume.stock_quantity > 0 ? 'В наличии' : 'Нет в наличии'}
                </p>
              </div>
              <div className="min-w-0">
                <span className="text-xs sm:text-sm text-gray-600 block mb-1">На складе</span>
                <p className="font-medium text-sm sm:text-base break-words">{perfume.stock_quantity} шт.</p>
              </div>
            </div>

            <div className="border-t pt-6">
              <div className="flex items-center justify-between mb-4 gap-2">
                <span className="font-medium flex-shrink-0">Количество:</span>
                <div className="flex items-center space-x-3 flex-shrink-0">
                  <button
                    onClick={decreaseQuantity}
                    disabled={quantity <= 1}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                  >
                    -
                  </button>
                  <span className="w-8 text-center font-medium">{quantity}</span>
                  <button
                    onClick={increaseQuantity}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                  >
                    +
                  </button>
                </div>
              </div>

              <Button
                variant="primary"
                size="lg"
                className="w-full"
                loading={isAdding}
                disabled={perfume.stock_quantity === 0}
                onClick={handleAddToCart}
              >
                {perfume.stock_quantity === 0 ? 'Нет в наличии' : `Добавить ${quantity} шт. в корзину`}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};