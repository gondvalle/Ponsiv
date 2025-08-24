import { useEffect } from 'react';
import { useAuth } from '@/react-app/auth-shim';
import { useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

export default function AuthCallback() {
  const { exchangeCodeForSessionToken } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        await exchangeCodeForSessionToken();
        navigate('/');
      } catch (error) {
        console.error('Authentication failed:', error);
        navigate('/');
      }
    };

    handleCallback();
  }, [exchangeCodeForSessionToken, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="text-center">
        <div className="animate-spin mb-4">
          <Loader2 className="w-12 h-12 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white mb-2">Autenticando...</h2>
        <p className="text-blue-200">Te estamos llevando a Ponsiv</p>
      </div>
    </div>
  );
}
