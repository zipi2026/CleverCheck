import { Navigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { useAuthStore } from '../store/authStore';

export const LoginPage = () => {
  const isAuthenticated = useAuthStore((state: { isAuthenticated: boolean }) => state.isAuthenticated);
  const loading = useAuthStore((state: { loading: boolean }) => state.loading);

  if (loading) {
    return <div className="page-loading">בודק כניסה…</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="login-page" dir="rtl">
      <div className="login-hero">
        <p className="eyebrow">CleverCheck</p>
        <h1>מערכת מבחנים חכמה ונוחה</h1>
        <p>עבודה על מבחנים, שמירה אוטומטית וסקירת תוצאות מכל מקום.</p>
      </div>
      <div className="login-card">
        <LoginForm />
      </div>
    </div>
  );
};
