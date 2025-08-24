import { useAuth } from '@getmocha/users-service/react';
import { Sparkles, Shirt, Heart, Users } from 'lucide-react';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const { redirectToLogin } = useAuth();

  if (!isOpen) return null;

  const handleLogin = async () => {
    try {
      await redirectToLogin();
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      
      <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-white/10 shadow-2xl">
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Bienvenido a Ponsiv</h2>
          <p className="text-gray-300">Descubre, organiza y compra moda de forma inteligente</p>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-2 bg-purple-500/20 rounded-xl flex items-center justify-center">
              <Heart className="w-6 h-6 text-purple-400" />
            </div>
            <p className="text-xs text-gray-400">Feed personalizado</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-2 bg-blue-500/20 rounded-xl flex items-center justify-center">
              <Shirt className="w-6 h-6 text-blue-400" />
            </div>
            <p className="text-xs text-gray-400">Armario virtual</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 mx-auto mb-2 bg-pink-500/20 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-pink-400" />
            </div>
            <p className="text-xs text-gray-400">Outfits sociales</p>
          </div>
        </div>

        <button
          onClick={handleLogin}
          className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105 flex items-center justify-center gap-3"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Continuar con Google
        </button>

        <p className="text-xs text-gray-500 text-center mt-4">
          Al continuar, aceptas nuestros términos de servicio y política de privacidad
        </p>
      </div>
    </div>
  );
}
