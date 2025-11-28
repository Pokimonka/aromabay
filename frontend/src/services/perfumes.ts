import { api } from './api';
import type { Perfume } from '../types';

export const perfumeService = {
  // Получить все духи
  getPerfumes: async (params?: {
    search?: string;
    sort?: string;
    page?: number;
  }) => {
    const response = await api.get('/api/v1/perfumes/', { params });
    return response.data;
  },

  // Получить один товар
  getPerfume: async (id: number): Promise<Perfume> => {
    const response = await api.get(`/api/v1/perfumes/${id}`);
    return response.data;
  },

  // Создать товар (админ)
  createPerfume: async (perfume: Omit<Perfume, 'id' | 'createdAt'>) => {
    const response = await api.post('/api/v1/perfumes/', perfume);
    return response.data;
  },

  // Обновить товар (админ)
  updatePerfume: async (id: number, perfume: Partial<Perfume>) => {
    const response = await api.put(`/api/v1/perfumes/${id}`, perfume);
    return response.data;
  },

  // Удалить товар (админ)
  deletePerfume: async (id: number) => {
    const response = await api.delete(`/api/v1/perfumes/${id}`);
    return response.data;
  },
};