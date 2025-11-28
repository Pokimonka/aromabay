import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, LoginData, RegisterData } from '../types';
import { authService } from '../services/auth';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Проверка аутентификации при загрузке
  // useEffect(() => {
  //   checkAuth();
  // }, []);

  // const checkAuth = async () => {
  //   if (true) {
  //     try {
  //       const userData = await authService.getCurrentUser();
  //       setUser(userData);
  //     } catch (error) {
  //       localStorage.removeItem('authToken');
  //     }
  //   }
  //   setIsLoading(false);
  // };

  useEffect(() => {
    const initAuth = async () => {
      setIsLoading(true);
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        setUser(null);
        // Игнорируем ошибку - пользователь просто не авторизован
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []); // Пустой массив зависимостей - выполняется только один раз

  const login = async (data: LoginData) => {
    await authService.login(data);
    const userData = await authService.getCurrentUser();
    setUser(userData);
  };

  const register = async (data: RegisterData) => {
    await authService.register(data);
    const userData = await authService.getCurrentUser();
    setUser(userData);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  const value = {
    user,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};