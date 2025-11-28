import React, { useState } from 'react';
import { usePerfumes } from '../hooks/usePerfumes';
import { perfumeService } from '../services/perfumes';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import  { PerfumeType } from '../types';

export const Admin: React.FC = () => {
  const { perfumes, loading, refetch } = usePerfumes();
  const [isAdding, setIsAdding] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    perfumeType: PerfumeType.FLORAL,
    stock_quantity: '',
    img_url: '',
    brand: '',
    volume: '',
    concentration: '',
  });

  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsAdding(true);
      await perfumeService.createPerfume({
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price),
        perfume_type: formData.perfumeType,
        stock_quantity: parseInt(formData.stock_quantity),
        img_url: formData.img_url || '',
        brand: formData.brand,
        volume: parseInt(formData.volume),
        concentration: formData.concentration,
      });
      
      setFormData({
        name: '',
        description: '',
        price: '',
        perfumeType: PerfumeType.FLORAL,
        stock_quantity: '',
        img_url: '',
        brand: '',
        volume: '',
        concentration: '',
      });
      setShowForm(false);
      refetch();
      alert('Товар успешно добавлен!');
    } catch (error) {
      console.error('Failed to add product:', error);
      alert('Ошибка при добавлении товара');
    } finally {
      setIsAdding(false);
    }
  };

  const handleDeleteProduct = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот товар?')) {
      try {
        await perfumeService.deletePerfume(id);
        refetch();
        alert('Товар успешно удален!');
      } catch (error) {
        console.error('Failed to delete product:', error);
        alert('Ошибка при удалении товара');
      }
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Админ-панель</h1>
          <p className="text-gray-600">Управление товарами магазина</p>
        </div>
        
        <Button
          onClick={() => setShowForm(true)}
        >
          Добавить товар
        </Button>
      </div>

      {/* Форма добавления товара */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">Добавить новый товар</h2>
            
            <form onSubmit={handleAddProduct} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Название"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  required
                />
                
                <Input
                  label="Бренд"
                  value={formData.brand}
                  onChange={(e) => setFormData(prev => ({ ...prev, brand: e.target.value }))}
                  required
                />
                
                <Input
                  label="Цена (руб)"
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                  required
                />
                
                <Input
                  label="Количество на складе"
                  type="number"
                  value={formData.stock_quantity}
                  onChange={(e) => setFormData(prev => ({ ...prev, stock_quantity: e.target.value }))}
                  required
                />
                
                <Input
                  label="Объем (мл)"
                  type="number"
                  value={formData.volume}
                  onChange={(e) => setFormData(prev => ({ ...prev, volume: e.target.value }))}
                  required
                />
                
                <Input
                  label="Концентрация"
                  value={formData.concentration}
                  onChange={(e) => setFormData(prev => ({ ...prev, concentration: e.target.value }))}
                  placeholder="EDP, EDT, Parfum"
                  required
                />
              </div>
              
              <div>
                <Input
                  label="URL изображения"
                  type="url"
                  value={formData.img_url}
                  onChange={(e) => setFormData(prev => ({ ...prev, img_url: e.target.value }))}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Описание
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
              
              <div className="flex justify-end space-x-3 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowForm(false)}
                >
                  Отмена
                </Button>
                <Button
                  type="submit"
                  loading={isAdding}
                >
                  Добавить товар
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Список товаров */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Товар
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Цена
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  На складе
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Действия
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {perfumes.map(perfume => (
                <tr key={perfume.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-gray-200 rounded-lg flex-shrink-0 mr-3">
                        <img
                          src={perfume.img_url || '/api/placeholder/40/40'}
                          alt={perfume.name}
                          className="w-full h-full object-cover rounded-lg"
                        />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {perfume.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {perfume.brand}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {perfume.price.toLocaleString()} ₽
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      perfume.stock_quantity > 10 
                        ? 'bg-green-100 text-green-800'
                        : perfume.stock_quantity > 0
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {perfume.stock_quantity} шт.
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => handleDeleteProduct(perfume.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {perfumes.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Товары не найдены</p>
          <p className="text-gray-400">Добавьте первый товар используя кнопку выше</p>
        </div>
      )}
    </div>
  );
};