import { api } from './api';
import { AuthResponse, LoginData, RegisterData, User } from '../types';

export const authService = {
  // Регистрация
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/api/v1/auth/register', data);
    return response.data;
  },

  // Авторизация
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/api/v1/auth/login', data);
    return response.data;
  },

  // Получение текущего пользователя
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/v1/auth/me');
    return response.data;
  },

  // Выход
  logout: async (): Promise<void> => {
    const response = await api.post('/api/v1/auth/logout');
    return response.data;
  },
};

const getCookie = (name: string): string | null => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
};

// Интерцептор для добавления токена к запросам
api.interceptors.request.use((config) => {
  const token = getCookie('session_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Интерцептор для обработки 401 ошибки
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Удаляем куку если она есть (невалидная сессия)
      document.cookie = 'session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      // НЕ делаем автоматический редирект - пусть компоненты сами решают, что делать
    }
    return Promise.reject(error);
  }
);