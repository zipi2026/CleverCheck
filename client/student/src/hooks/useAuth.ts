import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import { useAuthStore } from '../store/authStore';

export const useAuth = () => {
  const setUser = useAuthStore((state: { setUser: (user: any) => void }) => state.setUser);
  const setLoading = useAuthStore((state: { setLoading: (loading: boolean) => void }) => state.setLoading);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    authService
      .me()
      .then((user) => {
        setUser(user);
        if (location.pathname === '/' || location.pathname === '/login') {
          navigate('/dashboard', { replace: true });
        }
      })
      .catch(() => {
        setUser(null);
        if (location.pathname !== '/login') {
          navigate('/login', { replace: true });
        }
      })
      .finally(() => setLoading(false));
  }, [location.pathname, navigate, setLoading, setUser]);
};
