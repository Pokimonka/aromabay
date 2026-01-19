/**
 * Утилиты для работы с изображениями
 */

const BACKEND_URL = 'http://localhost:8000';
const PLACEHOLDER_PATH = '/src/images/placeholder.jpg';

/**
 * Получает полный URL изображения
 * Если URL уже полный (начинается с http), использует как есть
 * Если это относительный путь, добавляет базовый URL бэкенда
 */
export const getImageUrl = (url: string | undefined): string => {
  // Если URL уже полный (начинается с http), используем как есть
  if (url && url.startsWith('http')) {
    return url;
  }
  // Если это относительный путь, добавляем базовый URL бэкенда
  if (url && url.startsWith('/')) {
    return `${BACKEND_URL}${url}`;
  }
  // В противном случае, возвращаем как есть или placeholder
  return url || PLACEHOLDER_PATH;
};

/**
 * Обработчик ошибки загрузки изображения
 * Заменяет изображение на placeholder при ошибке
 */
export const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
  const target = e.target as HTMLImageElement;
  const placeholderPath = PLACEHOLDER_PATH;
  const currentSrc = target.src;
  
  // Предотвращаем бесконечный цикл ошибок
  if (!currentSrc.includes('placeholder.jpg')) {
    target.src = placeholderPath;
    // Если и placeholder не загрузился, скрываем изображение
    target.onerror = () => {
      target.style.display = 'none';
    };
  }
};

