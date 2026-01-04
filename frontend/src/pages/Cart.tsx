import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/common/Button';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { orderService } from '../services/order';
import { getImageUrl, handleImageError } from '../utils/imageUtils';

export const Cart: React.FC = () => {
  const { items, total, isLoading, updateQuantity, removeFromCart, clearCart, showAuthModalFunc } = useCart();
  const { isAuthenticated } = useAuth(); 
  const [isOrdering, setIsOrdering] = useState(false);

  const handleQuantityChange = async (perfumeId: number, newQuantity: number) => {
    try {
      if (newQuantity === 0) {
        await removeFromCart(perfumeId);
      } else {
        await updateQuantity(perfumeId, newQuantity);
      }
    } catch (error) {
      // Ошибка уже обработана в updateQuantity (показ уведомления)
      // Здесь просто игнорируем, чтобы не было необработанных ошибок
    }
  };

  const handleRemove = async (perfumeId: number) => {
    if (window.confirm('Удалить товар из корзины?')) {
      await removeFromCart(perfumeId);
    }
  };

  const handleOrder = async () => {
    if (!isAuthenticated) {
      showAuthModalFunc('checkout');
      return;
    }
    try {
      setIsOrdering(true);
      console.log(items)
      const orderItems = items.map(item => ({
        perfume_id: item.perfume.id,
        quantity: item.quantity,
        price: item.perfume.price
      }));

      await orderService.createOrder(orderItems);
      await clearCart();
      
      alert('Заказ успешно оформлен! Спасибо за покупку!');
    } catch (error) {
      console.error('Order failed:', error);
      alert('Ошибка при оформлении заказа. Попробуйте еще раз.');
    } finally {
      setIsOrdering(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Корзина пуста</h2>
          <p className="text-gray-600 mb-6">Добавьте товары из каталога</p>
          <Link
            to="/catalog"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Перейти в каталог
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Корзина</h1>
        <p className="text-gray-600">Проверьте ваш заказ перед оформлением</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Список товаров */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border">
            {items.map(item => (
              <div
                key={item.perfume.id}
                className="flex items-center p-4 border-b last:border-b-0"
              >
                {/* Изображение */}
                <div className="w-16 h-16 bg-gray-100 rounded-lg flex-shrink-0 mr-4 flex items-center justify-center overflow-hidden">
                  <img
                    key={item.perfume.id}
                    src={getImageUrl(item.perfume.img_url)}
                    alt={item.perfume.name}
                    className="max-w-full max-h-full object-contain"
                    loading="lazy"
                    onError={handleImageError}
                  />
                </div>

                {/* Информация о товаре */}
                <div className="flex-1 mr-4">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {item.perfume.name}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {item.perfume.price.toLocaleString()} ₽ × {item.quantity}
                  </p>
                  <p className="text-green-600 font-semibold">
                    {(item.perfume.price * item.quantity).toLocaleString()} ₽
                  </p>
                </div>

                {/* Управление количеством */}
                <div className="flex items-center space-x-2 mr-4">
                  <button
                    onClick={() => handleQuantityChange(item.perfume.id, item.quantity - 1)}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    -
                  </button>
                  <span className="w-8 text-center font-medium">
                    {item.quantity}
                  </span>
                  <button
                    onClick={() => handleQuantityChange(item.perfume.id, item.quantity + 1)}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    +
                  </button>
                </div>

                {/* Удаление */}
                <button
                  onClick={() => handleRemove(item.perfume.id)}
                  className="text-red-600 hover:text-red-700 p-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Итоги */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border p-6 sticky top-4">
            <h3 className="text-lg font-semibold mb-4">Итоги заказа</h3>
            
            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-600">Товары ({items.reduce((sum, item) => sum + item.quantity, 0)})</span>
                <span>{total.toLocaleString()} ₽</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Доставка</span>
                <span className="text-green-600">Бесплатно</span>
              </div>
              <div className="border-t pt-3">
                <div className="flex justify-between text-lg font-semibold">
                  <span>Итого</span>
                  <span>{total.toLocaleString()} ₽</span>
                </div>
              </div>
            </div>

            <Button
              variant="primary"
              size="lg"
              className="w-full"
              loading={isOrdering}
              onClick={handleOrder}
            >
              Оформить заказ
            </Button>

            <Link
              to="/catalog"
              className="block text-center text-blue-600 hover:text-blue-700 mt-4"
            >
              Продолжить покупки
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};