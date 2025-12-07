import React from 'react';
import { Button } from '../common/Button';
import { useCart } from '../../contexts/CartContext';
import { useAuth } from '../../contexts/AuthContext';

export const AuthModal: React.FC = () => {
  const { showAuthModal, pendingAction, hideAuthModal, executePendingAction } = useCart();
  const { isAuthenticated } = useAuth();

  if (!showAuthModal) return null;

  const getMessage = () => {
    if (pendingAction === 'add-to-cart') {
      return 'Чтобы добавить товар в корзину, необходимо авторизоваться';
    } else if (pendingAction === 'checkout') {
      return 'Чтобы оформить заказ, необходимо авторизоваться';
    }
    return 'Для выполнения этого действия необходимо авторизоваться';
  };

  const handleContinue = () => {
    if (isAuthenticated) {
      executePendingAction();
    } else {
      // Перенаправляем на страницу регистрации
      window.location.href = '/register?redirect=' + encodeURIComponent(window.location.pathname);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 className="text-xl font-semibold mb-4">Требуется авторизация</h3>
        
        <p className="text-gray-600 mb-6">
          {getMessage()}
        </p>

        <div className="flex flex-col space-y-3">
          <Button
            variant="primary"
            onClick={handleContinue}
            className="w-full"
          >
            {isAuthenticated ? 'Продолжить' : 'Зарегистрироваться'}
          </Button>
          
          <Button
            variant="outline"
            onClick={hideAuthModal}
            className="w-full"
          >
            Отмена
          </Button>
          
          {!isAuthenticated && (
            <div className="text-center">
              <span className="text-gray-500 text-sm">Уже есть аккаунт? </span>
              <button
                onClick={() => {
                  hideAuthModal();
                  window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
                }}
                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                Войти
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};