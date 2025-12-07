import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { useAuth } from '../contexts/AuthContext';

export const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';

  useEffect(() => {
    if (isAuthenticated) {
      navigate(redirect, { replace: true });
    }
  }, [isAuthenticated, navigate, redirect]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      setErrors({ 
        submit: 'Заполните все поля' 
      });
      return;
    }

    setIsLoading(true);
    try {
      await login({
        email: formData.email,
        password: formData.password,
      });
      
      navigate(redirect, { replace: true });
    } catch (error: any) {
      setErrors({ 
        submit: error.response?.data?.message || 'Неверный email или пароль' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors.submit) {
      setErrors({});
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
          Войдите в аккаунт
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Или{' '}
          <Link
            to={`/register?redirect=${encodeURIComponent(redirect)}`}
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            создайте новый аккаунт
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <Input
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <Input
              label="Пароль"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
            />

            {errors.submit && (
              <div className="text-red-600 text-sm text-center">
                {errors.submit}
              </div>
            )}

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              loading={isLoading}
            >
              Войти
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};