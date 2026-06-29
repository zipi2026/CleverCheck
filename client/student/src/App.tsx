import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { DashboardPage } from './pages/DashboardPage';
import { ExamPage } from './pages/ExamPage';
import { LoginPage } from './pages/LoginPage';
import { ResultsPage } from './pages/ResultsPage';

export const App = () => {
  useAuth();

  return (
    <div dir="rtl" style={{ minHeight: '100vh', direction: 'rtl' }}>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/exam/:examId" element={<ExamPage />} />
        <Route path="/results/:id" element={<ResultsPage />} />
      </Routes>
    </div>
  );
};

export default App;
