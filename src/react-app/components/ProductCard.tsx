import { useState } from 'react';
import { Heart, Bookmark, ShoppingBag, Shirt, Eye } from 'lucide-react';
import { Product } from '@/shared/types';

interface ProductCardProps {
  product: Product;
  onInteraction: (productId: number, type: 'like' | 'save' | 'have' | 'buy' | 'view') => void;
}

export default function ProductCard({ product, onInteraction }: ProductCardProps) {
  const [liked, setLiked] = useState(false);
  const [saved, setSaved] = useState(false);
  const [inWardrobe, setInWardrobe] = useState(false);

  const handleLike = () => {
    setLiked(!liked);
    onInteraction(product.id, 'like');
  };

  const handleSave = () => {
    setSaved(!saved);
    onInteraction(product.id, 'save');
  };

  const handleAddToWardrobe = () => {
    setInWardrobe(!inWardrobe);
    onInteraction(product.id, 'have');
  };

  const handleBuy = () => {
    onInteraction(product.id, 'buy');
    if (product.purchase_url) {
      window.open(product.purchase_url, '_blank');
    }
  };

  const handleTryAR = () => {
    onInteraction(product.id, 'view');
    // TODO: Implement AR functionality
    alert('Funcionalidad AR próximamente disponible');
  };

  return (
    <div className="relative w-full h-screen flex-shrink-0 bg-black overflow-hidden">
      {/* Product Image/Video */}
      <div className="absolute inset-0">
        {product.video_url ? (
          <video
            src={product.video_url}
            autoPlay
            loop
            muted
            playsInline
            className="w-full h-full object-cover"
          />
        ) : (
          <img
            src={product.image_url || 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=600&fit=crop'}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        )}
        
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/20" />
      </div>

      {/* Product Info */}
      <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
        <div className="mb-4">
          <h3 className="text-xl font-bold mb-1">{product.name}</h3>
          {product.brand && (
            <p className="text-sm text-gray-300 mb-1">{product.brand.name}</p>
          )}
          <p className="text-2xl font-bold text-purple-400">
            {product.price}€
          </p>
          {product.description && (
            <p className="text-sm text-gray-300 mt-2 line-clamp-2">
              {product.description}
            </p>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="absolute right-4 bottom-24 flex flex-col gap-4">
        <button
          onClick={handleLike}
          className={`w-12 h-12 rounded-full flex items-center justify-center backdrop-blur-md transition-all ${
            liked
              ? 'bg-red-500/80 text-white'
              : 'bg-black/40 text-white hover:bg-black/60'
          }`}
        >
          <Heart className={`w-6 h-6 ${liked ? 'fill-current' : ''}`} />
        </button>

        <button
          onClick={handleSave}
          className={`w-12 h-12 rounded-full flex items-center justify-center backdrop-blur-md transition-all ${
            saved
              ? 'bg-yellow-500/80 text-white'
              : 'bg-black/40 text-white hover:bg-black/60'
          }`}
        >
          <Bookmark className={`w-6 h-6 ${saved ? 'fill-current' : ''}`} />
        </button>

        <button
          onClick={handleAddToWardrobe}
          className={`w-12 h-12 rounded-full flex items-center justify-center backdrop-blur-md transition-all ${
            inWardrobe
              ? 'bg-green-500/80 text-white'
              : 'bg-black/40 text-white hover:bg-black/60'
          }`}
        >
          <Shirt className={`w-6 h-6 ${inWardrobe ? 'fill-current' : ''}`} />
        </button>

        <button
          onClick={handleBuy}
          className="w-12 h-12 rounded-full bg-purple-600/80 hover:bg-purple-700/80 text-white flex items-center justify-center backdrop-blur-md transition-all"
        >
          <ShoppingBag className="w-6 h-6" />
        </button>

        <button
          onClick={handleTryAR}
          className="w-12 h-12 rounded-full bg-blue-600/80 hover:bg-blue-700/80 text-white flex items-center justify-center backdrop-blur-md transition-all"
        >
          <Eye className="w-6 h-6" />
        </button>
      </div>

      {/* Brand Logo */}
      {product.brand?.logo_url && (
        <div className="absolute top-4 left-4">
          <img
            src={product.brand.logo_url}
            alt={product.brand.name}
            className="w-10 h-10 rounded-full bg-white/10 p-2 backdrop-blur-md"
          />
        </div>
      )}
    </div>
  );
}
