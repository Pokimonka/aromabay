import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  className = '',
  onClick,
  ...props
}) => {
  const isDisabled = disabled || loading;
  const baseClasses = 'font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  // Возвращаем обычные цвета, для disabled используем inline styles
  const getVariantClasses = () => {
    if (isDisabled) {
      // Не добавляем hover классы для disabled кнопок
      return '';
    }
    
    switch (variant) {
      case 'primary':
        return 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500';
      case 'secondary':
        return 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500';
      case 'danger':
        return 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500';
      case 'outline':
        return 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-blue-500';
      default:
        return 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500';
    }
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  // Блокируем onClick, если кнопка disabled
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (isDisabled) {
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    onClick?.(e);
  };

  // Получаем inline стили для disabled состояния
  const getDisabledStyles = (): React.CSSProperties => {
    if (!isDisabled) return {};
    
    if (variant === 'outline') {
      return {
        backgroundColor: '#f9fafb',
        color: '#9ca3af',
        borderColor: '#e5e7eb',
        opacity: 0.6,
        cursor: 'not-allowed',
        pointerEvents: 'none',
      };
    }
    
    return {
      backgroundColor: '#d1d5db',
      color: '#6b7280',
      opacity: 0.6,
      cursor: 'not-allowed',
      pointerEvents: 'none',
    };
  };

  // Для disabled кнопок не применяем обычные классы стилей, используем только inline
  const variantClasses = isDisabled ? '' : getVariantClasses();
  
  const classes = `
    ${baseClasses}
    ${variantClasses}
    ${sizes[size]}
    ${isDisabled ? 'cursor-not-allowed' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  return (
    <button
      className={classes}
      style={getDisabledStyles()}
      disabled={isDisabled}
      onClick={handleClick}
      onMouseDown={(e) => {
        if (isDisabled) {
          e.preventDefault();
          e.stopPropagation();
        }
      }}
      {...props}
    >
      {loading ? (
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          Loading...
        </div>
      ) : (
        children
      )}
    </button>
  );
};