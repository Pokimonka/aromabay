import { api } from './api';
import type { CartItem } from '../types';

export const cartService = {
  getCart: async (): Promise<{ items: CartItem[] }> => {
    const response = await api.get('/api/v1/cart/');
    return response.data;
  },

  addToCart: async (perfumeId: number, quantity: number) => {
    const response = await api.post('/api/v1/cart/', {
      perfume_id: perfumeId,
      quantity,
    });
    return response.data;
  },

  updateQuantity: async (perfumeId: number, quantity: number) => {
    const response = await api.put(`/api/v1/cart/${perfumeId}`, {
      quantity,
    });
    return response.data;
  },

  removeFromCart: async (perfumeId: number) => {
    const response = await api.delete(`/api/v1/cart/${perfumeId}`);
    return response.data;
  },

  clearCart: async () => {
    const response = await api.delete('/api/v1/cart/');
    return response.data;
  },
};