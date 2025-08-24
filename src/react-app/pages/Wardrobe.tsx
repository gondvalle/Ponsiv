import { useState, useEffect } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import Layout from '@/react-app/components/Layout';
import { WardrobeItem } from '@/shared/types';
import { Plus, Upload, Tag, Search } from 'lucide-react';

export default function Wardrobe() {
  const { user } = useAuth();
  const [wardrobeItems, setWardrobeItems] = useState<WardrobeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    if (user) {
      loadWardrobe();
    }
  }, [user]);

  const loadWardrobe = async () => {
    try {
      const response = await fetch('/api/wardrobe');
      const data = await response.json();
      setWardrobeItems(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load wardrobe:', error);
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', name: 'Todo' },
    { id: 'tops', name: 'Camisetas' },
    { id: 'bottoms', name: 'Pantalones' },
    { id: 'dresses', name: 'Vestidos' },
    { id: 'shoes', name: 'Zapatos' },
    { id: 'accessories', name: 'Accesorios' },
  ];

  const filteredItems = wardrobeItems.filter(item => {
    const matchesSearch = searchTerm === '' || 
      (item.product?.name || item.custom_item_name || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = selectedCategory === 'all' || 
      (item.product?.category?.name || item.custom_item_category || '').toLowerCase().includes(selectedCategory);
    
    return matchesSearch && matchesCategory;
  });

  if (!user) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <p className="text-white text-xl">Inicia sesión para ver tu armario</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Mi Armario</h1>
          <p className="text-gray-300">Organiza y gestiona todas tus prendas</p>
        </div>

        {/* Search and Filters */}
        <div className="mb-6 space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar en tu armario..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div className="flex gap-2 overflow-x-auto pb-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Add Item Button */}
        <div className="mb-6">
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl transition-all transform hover:scale-105"
          >
            <Plus className="w-5 h-5" />
            Añadir prenda
          </button>
        </div>

        {/* Wardrobe Grid */}
        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="aspect-square bg-white/10 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-white/10 rounded-full flex items-center justify-center">
              <Upload className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">
              {searchTerm || selectedCategory !== 'all' ? 'No se encontraron prendas' : 'Tu armario está vacío'}
            </h3>
            <p className="text-gray-400 mb-6">
              {searchTerm || selectedCategory !== 'all' 
                ? 'Prueba con otros términos de búsqueda'
                : 'Comienza añadiendo tus primeras prendas'
              }
            </p>
            {(!searchTerm && selectedCategory === 'all') && (
              <button
                onClick={() => setShowAddModal(true)}
                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition-colors"
              >
                Añadir primera prenda
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {filteredItems.map((item) => (
              <div
                key={item.id}
                className="group relative aspect-square bg-white/5 rounded-xl overflow-hidden border border-white/10 hover:border-purple-400/50 transition-all cursor-pointer"
              >
                <img
                  src={
                    item.product?.image_url || 
                    item.custom_item_image_url || 
                    'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop'
                  }
                  alt={item.product?.name || item.custom_item_name || 'Prenda'}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                
                <div className="absolute bottom-0 left-0 right-0 p-3 text-white transform translate-y-full group-hover:translate-y-0 transition-transform">
                  <h4 className="font-semibold text-sm truncate">
                    {item.product?.name || item.custom_item_name}
                  </h4>
                  <p className="text-xs text-gray-300 truncate">
                    {item.product?.brand?.name || item.custom_item_brand || 'Sin marca'}
                  </p>
                  {item.product?.price && (
                    <p className="text-xs text-purple-400 font-medium">
                      {item.product.price}€
                    </p>
                  )}
                </div>

                {item.tags && (() => {
                  try {
                    const parsedTags = JSON.parse(item.tags);
                    return Array.isArray(parsedTags) && parsedTags.length > 0;
                  } catch {
                    return false;
                  }
                })() && (
                  <div className="absolute top-2 right-2">
                    <Tag className="w-4 h-4 text-purple-400" />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Item Modal - Simple placeholder for now */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowAddModal(false)} />
          <div className="relative bg-slate-800 rounded-xl p-6 max-w-md w-full">
            <h3 className="text-xl font-bold text-white mb-4">Añadir prenda</h3>
            <p className="text-gray-300 mb-6">
              Funcionalidad de subida de imágenes y etiquetado automático próximamente disponible.
            </p>
            <button
              onClick={() => setShowAddModal(false)}
              className="w-full py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </Layout>
  );
}
