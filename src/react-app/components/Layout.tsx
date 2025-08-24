import { ReactNode } from 'react';
import { useAuth } from '@getmocha/users-service/react';
import { useNavigate, useLocation } from 'react-router';
import { Home, Shirt, Users, Heart, LogOut } from 'lucide-react';

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
    { icon: Home, label: 'Feed', path: '/' },
    { icon: Shirt, label: 'Armario', path: '/wardrobe' },
    { icon: Heart, label: 'Outfits', path: '/outfits' },
    { icon: Users, label: 'Social', path: '/social' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Ponsiv
          </h1>
          
          {user && (
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <img
                  src={user.google_user_data.picture || ''}
                  alt={user.google_user_data.name || ''}
                  className="w-8 h-8 rounded-full border-2 border-purple-400"
                />
                <span className="text-white text-sm hidden sm:block">
                  {user.google_user_data.given_name}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-white transition-colors"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          )}
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
                  <Icon className="w-6 h-6" />
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
