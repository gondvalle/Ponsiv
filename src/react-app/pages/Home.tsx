import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import Layout from '@/react-app/components/Layout';
import LoginModal from '@/react-app/components/LoginModal';
import ProductCard from '@/react-app/components/ProductCard';
import { Product } from '@/shared/types';
import { Loader2 } from 'lucide-react';

export default function Home() {
  const { user } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const containerRef = useRef<HTMLDivElement>(null);

  // Load initial feed
  useEffect(() => {
    if (!user) {
      setShowLoginModal(true);
      setLoading(false);
      return;
    }
    loadFeed();
  }, [user]);

  const loadFeed = async (pageNum = 1) => {
    try {
      const response = await fetch(`/api/feed?page=${pageNum}&limit=10`);
      const data = await response.json();
      
      if (pageNum === 1) {
        setProducts(data.products);
      } else {
        setProducts(prev => [...prev, ...data.products]);
      }
      
      setHasMore(data.hasMore);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load feed:', error);
      setLoading(false);
    }
  };

  // Handle scroll for infinite loading
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const scrollTop = container.scrollTop;
      const itemHeight = container.clientHeight;
      const newIndex = Math.round(scrollTop / itemHeight);
      
      if (newIndex !== currentIndex) {
        setCurrentIndex(newIndex);
        
        // Load more when near the end
        if (newIndex >= products.length - 3 && hasMore && !loading) {
          setPage(prev => prev + 1);
          loadFeed(page + 1);
        }
      }
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [currentIndex, products.length, hasMore, loading, page]);

  const handleInteraction = async (productId: number, type: 'like' | 'save' | 'have' | 'buy' | 'view') => {
    if (!user) return;

    try {
      await fetch('/api/interactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: productId,
          interaction_type: type,
          interaction_data: type === 'view' ? { timestamp: Date.now() } : undefined,
        }),
      });

      // Add to wardrobe automatically when user clicks "have"
      if (type === 'have') {
        await fetch('/api/wardrobe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product_id: productId }),
        });
      }
    } catch (error) {
      console.error('Failed to record interaction:', error);
    }
  };

  if (!user) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-screen px-6 text-center">
          <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-purple-500 to-pink-500 rounded-3xl flex items-center justify-center">
            <span className="text-3xl font-bold text-white">P</span>
          </div>
          <h1 className="text-4xl font-bold text-white mb-4">
            Bienvenido a Ponsiv
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-md">
            Descubre moda personalizada, organiza tu armario y conecta con la comunidad
          </p>
          <button
            onClick={() => setShowLoginModal(true)}
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105"
          >
            Empezar ahora
          </button>
        </div>
        <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />
      </Layout>
    );
  }
 
  if (loading && products.length === 0) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-screen">
          <div className="animate-spin mb-4">
            <Loader2 className="w-12 h-12 text-purple-400" />
          </div>
          <p className="text-white text-lg">Preparando tu feed personalizado...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div 
        ref={containerRef}
        className="h-screen overflow-y-scroll snap-y snap-mandatory scrollbar-hide"
        style={{ scrollBehavior: 'smooth' }}
      >
        {products.map((product) => (
          <div key={product.id} className="snap-start">
            <ProductCard 
              product={product}
              onInteraction={handleInteraction}
            />
          </div>
        ))}
        
        {loading && products.length > 0 && (
          <div className="h-screen flex items-center justify-center">
            <div className="animate-spin">
              <Loader2 className="w-12 h-12 text-purple-400" />
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
