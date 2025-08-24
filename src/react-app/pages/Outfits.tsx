import { useState, useEffect } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import Layout from '@/react-app/components/Layout';
import { Outfit } from '@/shared/types';
import { Plus, Heart, Share, Eye } from 'lucide-react';

export default function Outfits() {
  const { user } = useAuth();
  const [outfits, setOutfits] = useState<Outfit[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'my-outfits' | 'recommendations'>('my-outfits');

  useEffect(() => {
    if (user) {
      loadOutfits();
    }
  }, [user, activeTab]);

  const loadOutfits = async () => {
    try {
      const url = activeTab === 'my-outfits' ? '/api/outfits' : '/api/outfits?public=true';
      const response = await fetch(url);
      const data = await response.json();
      
      // Ensure data is always an array
      if (Array.isArray(data)) {
        setOutfits(data);
      } else if (data && Array.isArray(data.outfits)) {
        setOutfits(data.outfits);
      } else {
        console.warn('API returned non-array data:', data);
        setOutfits([]);
      }
      setLoading(false);
    } catch (error) {
      console.error('Failed to load outfits:', error);
      setOutfits([]);
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <p className="text-white text-xl">Inicia sesión para ver tus outfits</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Outfits</h1>
          <p className="text-gray-300">Crea y descubre combinaciones perfectas</p>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <div className="flex gap-1 bg-white/10 rounded-xl p-1">
            <button
              onClick={() => setActiveTab('my-outfits')}
              className={`flex-1 py-3 px-6 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'my-outfits'
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Mis Outfits
            </button>
            <button
              onClick={() => setActiveTab('recommendations')}
              className={`flex-1 py-3 px-6 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'recommendations'
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Recomendaciones
            </button>
          </div>
        </div>

        {/* Create Outfit Button */}
        {activeTab === 'my-outfits' && (
          <div className="mb-6">
            <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl transition-all transform hover:scale-105">
              <Plus className="w-5 h-5" />
              Crear outfit
            </button>
          </div>
        )}

        {/* Outfits Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="aspect-[3/4] bg-white/10 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : !Array.isArray(outfits) || outfits.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-white/10 rounded-full flex items-center justify-center">
              <Heart className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">
              {activeTab === 'my-outfits' ? 'No tienes outfits aún' : 'No hay recomendaciones disponibles'}
            </h3>
            <p className="text-gray-400 mb-6">
              {activeTab === 'my-outfits' 
                ? 'Comienza creando tu primer outfit con las prendas de tu armario'
                : 'Las recomendaciones aparecerán cuando tengas más prendas en tu armario'
              }
            </p>
            {activeTab === 'my-outfits' && (
              <button className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition-colors">
                Crear primer outfit
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.isArray(outfits) && outfits.map((outfit) => (
              <div
                key={outfit.id}
                className="group relative aspect-[3/4] bg-white/5 rounded-xl overflow-hidden border border-white/10 hover:border-purple-400/50 transition-all cursor-pointer"
              >
                <img
                  src={
                    outfit.image_url || 
                    'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400&h=500&fit=crop'
                  }
                  alt={outfit.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                
                <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                  <h4 className="font-semibold text-lg mb-1">{outfit.name}</h4>
                  {outfit.description && (
                    <p className="text-sm text-gray-300 mb-3 line-clamp-2">
                      {outfit.description}
                    </p>
                  )}
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-sm">
                      <div className="flex items-center gap-1">
                        <Heart className="w-4 h-4" />
                        <span>{outfit.likes_count}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Eye className="w-4 h-4" />
                        <span>23</span>
                      </div>
                    </div>
                    
                    <button className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors">
                      <Share className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {outfit.is_public && (
                  <div className="absolute top-3 right-3">
                    <div className="px-2 py-1 bg-green-500/80 text-white text-xs rounded-full">
                      Público
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Floating Action Button for mobile */}
        {activeTab === 'my-outfits' && (
          <button className="fixed bottom-24 right-6 w-14 h-14 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all transform hover:scale-110 md:hidden">
            <Plus className="w-6 h-6" />
          </button>
        )}
      </div>
    </Layout>
  );
}
