import { api } from './api';
import type { Order } from '../types';

export const orderService = {
  createOrder: async (items: { perfume_id: number; quantity: number }[]) => {
    const response = await api.post('/api/v1/orders/', { items });
    return response.data;
  },

  getOrders: async (): Promise<Order[]> => {
    const response = await api.get('/api/v1/orders/');
    return response.data;
  },

  getOrder: async (id: number): Promise<Order> => {
    const response = await api.get(`/api/v1/orders/${id}`);
    return response.data;
  },
};