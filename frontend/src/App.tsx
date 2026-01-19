import  { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider, useCart } from './contexts/CartContext';
import { AuthProvider } from './contexts/AuthContext';
import { Header } from './components/layout/Header';
import { AuthModal } from './components/auth/AuthModal';
import { Toast } from './components/common/Toast';
import { Home } from './pages/Home';
import { Catalog } from './pages/Catalog';
import { Cart } from './pages/Cart';
import { Admin } from './pages/Admin';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ProductDetail } from './pages/ProductDetail';
import { Perfume } from './types';

function AppContent() {
  const [currentProduct, setCurrentProduct] = useState<Perfume | null>(null);
  const { toastMessage, hideToast } = useCart();

  const handleViewProduct = (perfume: Perfume) => {
    setCurrentProduct(perfume);
  };

  const handleCloseProduct = () => {
    setCurrentProduct(null);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route 
              path="/catalog" 
              element={<Catalog onViewProduct={handleViewProduct} />} 
            />
            <Route path="/cart" element={<Cart />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>

        {/* Модальное окно авторизации */}
        <AuthModal />

        {/* Всплывающее уведомление */}
        <Toast 
          message={toastMessage || ''} 
          isVisible={!!toastMessage}
          onClose={hideToast}
        />

        {/* Модальное окно деталей товара */}
        {currentProduct && (
          <ProductDetail
            perfume={currentProduct}
            onClose={handleCloseProduct}
          />
        )}
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <AppContent />
      </CartProvider>
    </AuthProvider>
  );
}

export default App;