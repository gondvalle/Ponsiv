import { useState, useEffect } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import Layout from '@/react-app/components/Layout';
import { Outfit } from '@/shared/types';
import { Heart, MessageCircle, Share, Bookmark, TrendingUp, Users, Sparkles } from 'lucide-react';

export default function Social() {
  const { user } = useAuth();
  const [publicOutfits, setPublicOutfits] = useState<Outfit[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState<'trending' | 'recent' | 'following'>('trending');

  useEffect(() => {
    if (user) {
      loadPublicOutfits();
    }
  }, [user, activeFilter]);

  const loadPublicOutfits = async () => {
    try {
      const response = await fetch('/api/outfits?public=true');
      const data = await response.json();
      setPublicOutfits(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load public outfits:', error);
      setLoading(false);
    }
  };

  const filters = [
    { id: 'trending', name: 'Trending', icon: TrendingUp },
    { id: 'recent', name: 'Recientes', icon: Sparkles },
    { id: 'following', name: 'Siguiendo', icon: Users },
  ];

  if (!user) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <p className="text-white text-xl">Inicia sesión para explorar la comunidad</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Comunidad</h1>
          <p className="text-gray-300">Descubre los outfits más populares de la comunidad</p>
        </div>

        {/* Filters */}
        <div className="mb-6 flex gap-2 overflow-x-auto pb-2">
          {filters.map(({ id, name, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveFilter(id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                activeFilter === id
                  ? 'bg-purple-600 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              <Icon className="w-4 h-4" />
              {name}
            </button>
          ))}
        </div>

        {/* Feed */}
        {loading ? (
          <div className="space-y-6">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white/5 rounded-xl p-6 animate-pulse">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-white/20 rounded-full" />
                  <div className="flex-1">
                    <div className="h-4 bg-white/20 rounded w-32 mb-2" />
                    <div className="h-3 bg-white/20 rounded w-24" />
                  </div>
                </div>
                <div className="aspect-square bg-white/20 rounded-lg mb-4" />
                <div className="h-4 bg-white/20 rounded w-3/4" />
              </div>
            ))}
          </div>
        ) : publicOutfits.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-white/10 rounded-full flex items-center justify-center">
              <Users className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">
              No hay outfits públicos aún
            </h3>
            <p className="text-gray-400">
              Sé el primero en compartir un outfit con la comunidad
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {publicOutfits.map((outfit) => (
              <div
                key={outfit.id}
                className="bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:border-purple-400/30 transition-colors"
              >
                {/* User Header */}
                <div className="p-4 flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {outfit.user_id.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="flex-1">
                    <h4 className="text-white font-semibold">Usuario {outfit.user_id.slice(0, 8)}</h4>
                    <p className="text-gray-400 text-sm">Hace 2 horas</p>
                  </div>
                  <button className="p-2 text-gray-400 hover:text-white transition-colors">
                    <Share className="w-5 h-5" />
                  </button>
                </div>

                {/* Outfit Image */}
                <div className="aspect-square relative">
                  <img
                    src={
                      outfit.image_url || 
                      'https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&h=600&fit=crop'
                    }
                    alt={outfit.name}
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* Outfit Info */}
                <div className="p-4">
                  <h3 className="text-white font-semibold text-lg mb-2">{outfit.name}</h3>
                  {outfit.description && (
                    <p className="text-gray-300 mb-4">{outfit.description}</p>
                  )}

                  {/* Actions */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-6">
                      <button className="flex items-center gap-2 text-gray-400 hover:text-red-400 transition-colors">
                        <Heart className="w-6 h-6" />
                        <span className="text-sm">{outfit.likes_count}</span>
                      </button>
                      <button className="flex items-center gap-2 text-gray-400 hover:text-blue-400 transition-colors">
                        <MessageCircle className="w-6 h-6" />
                        <span className="text-sm">5</span>
                      </button>
                      <button className="text-gray-400 hover:text-purple-400 transition-colors">
                        <Share className="w-6 h-6" />
                      </button>
                    </div>
                    <button className="text-gray-400 hover:text-yellow-400 transition-colors">
                      <Bookmark className="w-6 h-6" />
                    </button>
                  </div>

                  {/* Tags */}
                  <div className="mt-4 flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-purple-600/20 text-purple-300 text-xs rounded-full">
                      #casual
                    </span>
                    <span className="px-3 py-1 bg-blue-600/20 text-blue-300 text-xs rounded-full">
                      #streetwear
                    </span>
                    <span className="px-3 py-1 bg-pink-600/20 text-pink-300 text-xs rounded-full">
                      #trendy
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
