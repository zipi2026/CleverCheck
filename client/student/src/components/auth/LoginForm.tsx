import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';

export const LoginForm = () => {
  const navigate = useNavigate();
  const [id, setId] = useState('student01');
  const [password, setPassword] = useState('password');
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authService.login({ id, password, rememberMe });
      navigate('/dashboard', { replace: true });
    } catch {
      setError('הכניסה נכשלה. נסו שוב.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h2>כניסת תלמיד</h2>
      {error ? <div className="form-error">{error}</div> : null}
      <label>
        מספר תלמיד
        <input value={id} onChange={(event) => setId(event.target.value)} />
      </label>
      <label>
        סיסמה
        <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
      </label>
      <label className="checkbox-row">
        <input type="checkbox" checked={rememberMe} onChange={(event) => setRememberMe(event.target.checked)} />
        זכור אותי
      </label>
      <button type="submit" className="primary-button" disabled={loading}>
        {loading ? 'מתחבר…' : 'התחברות'}
      </button>
    </form>
  );
};
