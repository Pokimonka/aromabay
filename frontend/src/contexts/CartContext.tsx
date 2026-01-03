import React, { createContext, useContext, useReducer, useEffect } from 'react';
import type { CartItem, Perfume } from '../types';
import { cartService } from '../services/cart';
import { useAuth } from './AuthContext';

interface CartState {
  items: CartItem[];
  total: number;
  isLoading: boolean;
  showAuthModal: boolean;
  pendingAction: 'add-to-cart' | 'checkout' | null;
  pendingPerfume?: Perfume;
  outOfStockItems: number[]; // IDs товаров, которые недоступны
  toastMessage: string | null; // Сообщение для всплывающего уведомления
}

type CartAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ITEMS'; payload: CartItem[] }
  | { type: 'ADD_ITEM'; payload: Perfume }
  | { type: 'REMOVE_ITEM'; payload: number }
  | { type: 'UPDATE_QUANTITY'; payload: { id: number; quantity: number } }
  | { type: 'CLEAR_CART' }
  | { type: 'SHOW_AUTH_MODAL'; payload: { action: 'add-to-cart' | 'checkout'; perfume?: Perfume } }
  | { type: 'HIDE_AUTH_MODAL' }
  | { type: 'SET_OUT_OF_STOCK'; payload: number } // perfume ID
  | { type: 'REMOVE_OUT_OF_STOCK'; payload: number } // perfume ID
  | { type: 'CLEAR_OUT_OF_STOCK' } // очистить весь список
  | { type: 'SHOW_TOAST'; payload: string } // показать уведомление
  | { type: 'HIDE_TOAST' }; // скрыть уведомление

// Убираем extends CartState и явно перечисляем все свойства
interface CartContextType {
  // Свойства из CartState
  items: CartItem[];
  total: number;
  isLoading: boolean;
  showAuthModal: boolean;
  pendingAction: 'add-to-cart' | 'checkout' | null;
  pendingPerfume?: Perfume;
  
  // Методы
  addToCart: (perfume: Perfume) => Promise<void>;
  removeFromCart: (perfumeId: number) => Promise<void>;
  updateQuantity: (perfumeId: number, quantity: number) => Promise<void>;
  clearCart: () => Promise<void>;
  getTotalItems: () => number;
  showAuthModalFunc: (action: 'add-to-cart' | 'checkout', perfume?: Perfume) => void; // Переименовываем
  hideAuthModal: () => void;
  executePendingAction: () => Promise<void>;
  isOutOfStock: (perfumeId: number) => boolean;
  toastMessage: string | null;
  hideToast: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const cartReducer = (state: CartState, action: CartAction): CartState => {
  switch (action.type) {
    case 'SHOW_AUTH_MODAL':
      return {
        ...state,
        showAuthModal: true,
        pendingAction: action.payload.action,
        pendingPerfume: action.payload.perfume,
      };
    case 'HIDE_AUTH_MODAL':
      return {
        ...state,
        showAuthModal: false,
        pendingAction: null,
        pendingPerfume: undefined,
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    
    case 'SET_ITEMS':
      const total = action.payload.reduce((sum, item) => 
        sum + (item.perfume.price * item.quantity), 0
      );
      return { ...state, items: action.payload, total };
    
    case 'ADD_ITEM':
      const existingItem = state.items.find(item => 
        item.perfume.id === action.payload.id
      );
      
      if (existingItem) {
        const updatedItems = state.items.map(item =>
          item.perfume.id === action.payload.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
        const total = updatedItems.reduce((sum, item) => 
          sum + (item.perfume.price * item.quantity), 0
        );
        return { ...state, items: updatedItems, total };
      } else {
        const newItem = { 
          id: Date.now(), // Добавляем недостающие свойства
          order_id: 0, // временное значение
          perfume: action.payload, 
          quantity: 1,
          price: action.payload.price // дублируем цену для удобства
        };
        const updatedItems = [...state.items, newItem];
        const total = updatedItems.reduce((sum, item) => 
          sum + (item.perfume.price * item.quantity), 0
        );
        return { ...state, items: updatedItems, total };
      }
    
    case 'REMOVE_ITEM':
      const filteredItems = state.items.filter(
        item => item.perfume.id !== action.payload
      );
      const totalAfterRemove = filteredItems.reduce((sum, item) => 
        sum + (item.perfume.price * item.quantity), 0
      );
      return { ...state, items: filteredItems, total: totalAfterRemove };
    
    case 'UPDATE_QUANTITY':
      const updatedItems = state.items.map(item =>
        item.perfume.id === action.payload.id
          ? { ...item, quantity: action.payload.quantity }
          : item
      ).filter(item => item.quantity > 0);
      
      const totalAfterUpdate = updatedItems.reduce((sum, item) => 
        sum + (item.perfume.price * item.quantity), 0
      );
      return { ...state, items: updatedItems, total: totalAfterUpdate };
    
    case 'CLEAR_CART':
      return { ...state, items: [], total: 0, outOfStockItems: [] };
    
    case 'SET_OUT_OF_STOCK':
      if (state.outOfStockItems.includes(action.payload)) {
        return state;
      }
      return { ...state, outOfStockItems: [...state.outOfStockItems, action.payload] };
    
    case 'REMOVE_OUT_OF_STOCK':
      return { 
        ...state, 
        outOfStockItems: state.outOfStockItems.filter(id => id !== action.payload) 
      };
    
    case 'CLEAR_OUT_OF_STOCK':
      return { ...state, outOfStockItems: [] };
    
    case 'SHOW_TOAST':
      return { ...state, toastMessage: action.payload };
    
    case 'HIDE_TOAST':
      return { ...state, toastMessage: null };
    
    default:
      return state;
  }
};

const initialState: CartState = {
  items: [],
  total: 0,
  isLoading: false,
  showAuthModal: false,
  pendingAction: null,
  outOfStockItems: [],
  toastMessage: null,
};

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  useEffect(() => {
    // Не загружаем корзину, пока идет проверка авторизации
    if (authLoading) return;
    
    if (isAuthenticated) {
      loadCart();
    } else {
      dispatch({ type: 'SET_ITEMS', payload: [] });
      // Очищаем список недоступных товаров при разлогине
      dispatch({ type: 'CLEAR_OUT_OF_STOCK' });
    }
  }, [isAuthenticated, authLoading]);

  const loadCart = async () => {
    if (!isAuthenticated) return;
    
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const cartData = await cartService.getCart();
      dispatch({ type: 'SET_ITEMS', payload: cartData.items || [] });
    } catch (error) {
      console.error('Failed to load cart:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }

  const addToCart = async (perfume: Perfume) => {
    if (!isAuthenticated) {
      showAuthModalFunc('add-to-cart', perfume);
      return;
    }

    try {
      await cartService.addToCart(perfume.id, 1);
      dispatch({ type: 'ADD_ITEM', payload: perfume });
      // Убираем товар из списка недоступных, если он был там (на случай, если он снова появился)
      if (state.outOfStockItems.includes(perfume.id)) {
        dispatch({ type: 'REMOVE_OUT_OF_STOCK', payload: perfume.id });
      }
    } catch (error: any) {
      console.error('Failed to add to cart:', error);
      // Проверяем, является ли это ошибкой 409 с detail "OUT_OF_STOCK"
      const status = error?.response?.status || error?.status;
      const detail = error?.response?.data?.detail || error?.response?.data?.message || error?.message;
      
      if (status === 409) {
        // Проверяем регистронезависимо
        const detailStr = String(detail || '').toUpperCase();
        if (detailStr === 'OUT_OF_STOCK' || detailStr.includes('OUT_OF_STOCK') || detailStr.includes('OUT OF STOCK')) {
          // Показываем уведомление (не блокируем кнопку, чтобы можно было попробовать снова после удаления из корзины)
          dispatch({ type: 'SHOW_TOAST', payload: 'Больше товара добавить нельзя, не хватает на складе' });
        }
      }
      throw error;
    }
  };

  const executePendingAction = async () => {
    if (!state.pendingAction || !isAuthenticated) return;

    try {
      if (state.pendingAction === 'add-to-cart' && state.pendingPerfume) {
        await addToCart(state.pendingPerfume);
      }
    } finally {
      dispatch({ type: 'HIDE_AUTH_MODAL' });
    }
  };

  const showAuthModalFunc = (action: 'add-to-cart' | 'checkout', perfume?: Perfume) => {
    dispatch({ type: 'SHOW_AUTH_MODAL', payload: { action, perfume } });
  };

  const hideAuthModal = () => {
    dispatch({ type: 'HIDE_AUTH_MODAL' });
  };

  const removeFromCart = async (perfumeId: number) => {
    try {
      await cartService.removeFromCart(perfumeId);
      dispatch({ type: 'REMOVE_ITEM', payload: perfumeId });
    } catch (error) {
      console.error('Failed to remove from cart:', error);
      throw error;
    }
  };

  const updateQuantity = async (perfumeId: number, quantity: number) => {
    try {
      await cartService.updateQuantity(perfumeId, quantity);
      dispatch({ type: 'UPDATE_QUANTITY', payload: { id: perfumeId, quantity } });
    } catch (error) {
      console.error('Failed to update quantity:', error);
      throw error;
    }
  };

  const clearCart = async () => {
    try {
      await cartService.clearCart();
      dispatch({ type: 'CLEAR_CART' });
    } catch (error) {
      console.error('Failed to clear cart:', error);
      throw error;
    }
  };

  const getTotalItems = () => {
    return state.items.reduce((total, item) => total + item.quantity, 0);
  };

  const isOutOfStock = (perfumeId: number) => {
    return state.outOfStockItems.includes(perfumeId);
  };

  const hideToast = () => {
    dispatch({ type: 'HIDE_TOAST' });
  };

  return (
    <CartContext.Provider value={{
      ...state,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalItems,
      showAuthModalFunc,
      hideAuthModal,
      executePendingAction,
      isOutOfStock,
      hideToast,
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};