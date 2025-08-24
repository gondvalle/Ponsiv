import { ReactNode } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import { useNavigate, useLocation } from 'react-router';
import {
  Home,
  Hanger,
  Tshirt,
  ShoppingBag,
  Bell,
  MessageCircle,
  LogOut,
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/' },
    { icon: Hanger, label: 'Looks', path: '/looks' },
    { icon: Tshirt, label: 'Feed', path: '/feed' },
    { icon: ShoppingBag, label: 'Carrito', path: '/cart' },
    { icon: undefined, label: 'Perfil', path: '/profile' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-white">PONSIV</h1>

          <div className="flex items-center gap-4">
            <button aria-label="Notificaciones" className="relative text-white">
              <Bell className="w-6 h-6" />
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] rounded-full px-1">1</span>
            </button>
            <button aria-label="Mensajes" className="relative text-white">
              <MessageCircle className="w-6 h-6" />
            </button>
            {user && (
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-white transition-colors"
              >
                <LogOut className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-16 pb-20">
        {children}
      </main>

      {/* Bottom Navigation */}
      {user && (
        <nav className="fixed bottom-0 left-0 right-0 z-50 bg-black/30 backdrop-blur-md border-t border-white/10">
          <div className="max-w-screen-xl mx-auto px-4">
            <div className="flex justify-around py-2">
              {navItems.map(({ icon: Icon, label, path }) => (
                <button
                  key={path}
                  onClick={() => navigate(path)}
                  className={`flex flex-col items-center gap-1 py-2 px-4 rounded-lg transition-colors ${
                    location.pathname === path
                      ? 'text-purple-400 bg-purple-400/10'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {Icon ? (
                    <Icon className="w-6 h-6" />
                  ) : (
                    <img
                      src={user?.google_user_data.picture || ''}
                      alt="avatar"
                      className="w-6 h-6 rounded-full border border-white"
                    />
                  )}
                  <span className="text-xs font-medium">{label}</span>
                </button>
              ))}
            </div>
          </div>
        </nav>
      )}
    </div>
  );
}
