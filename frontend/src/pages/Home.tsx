import React from 'react';
import { Link } from 'react-router-dom';
import { usePerfumes } from '../hooks/usePerfumes';
import { PerfumeCard } from '../components/features/perfumes/PerfumeCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import type { Perfume } from '../types';

export const Home: React.FC = () => {
  const { perfumes, loading } = usePerfumes();
  const featuredPerfumes = perfumes.slice(0, 4);

  const handleViewProduct = (perfume: Perfume) => {
    // В реальном приложении здесь была бы навигация
    console.log('View product:', perfume);
    alert(`Просмотр товара: ${perfume.name}`);
  };

  return (
    <div>
      {/* Hero секция */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Мир изысканных ароматов
          </h1>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Откройте для себя уникальные парфюмерные композиции, созданные для настоящих ценителей
          </p>
          <Link
            to="/catalog"
            className="inline-flex items-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
          >
            Исследовать каталог
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </div>
      </section>

      {/* Популярные товары */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Популярные ароматы
            </h2>
            <p className="text-gray-600 text-lg">
              Самые востребованные парфюмы нашей коллекции
            </p>
          </div>

          {loading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {featuredPerfumes.map(perfume => (
                <PerfumeCard
                  key={perfume.id}
                  perfume={perfume}
                  onViewDetails={handleViewProduct}
                />
              ))}
            </div>
          )}

          <div className="text-center">
            <Link
              to="/catalog"
              className="inline-flex items-center px-6 py-3 border border-blue-600 text-blue-600 font-medium rounded-lg hover:bg-blue-50 transition-colors"
            >
              Смотреть все товары
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Преимущества */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Гарантия качества</h3>
              <p className="text-gray-600">Только оригинальная продукция от официальных дистрибьюторов</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Быстрая доставка</h3>
              <p className="text-gray-600">Доставка по всей России от 1 дня</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Консультация</h3>
              <p className="text-gray-600">Поможем подобрать аромат именно для вас</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};