import { useEffect, useState } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { examService } from '../services/examService';
import { useAuthStore } from '../store/authStore';
import type { ResultsPayload } from '../types';

export const ResultsPage = () => {
  const { id } = useParams();
  const isAuthenticated = useAuthStore((state: { isAuthenticated: boolean }) => state.isAuthenticated);
  const loading = useAuthStore((state: { loading: boolean }) => state.loading);
  const [results, setResults] = useState<ResultsPayload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
  if (!id) return;

    examService
      .getResults(id)
      .then((data) => {
        setResults(data);
        setError(null);
      })
      .catch((err) => {
        setResults(null);
        setError(err.message || 'אין נתונים על המבחן');
      });
  }, [id]);

  if (loading) {
    return <div className="page-loading">בודק כניסה…</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!results && !error) {
    return <div className="page-loading">טוען תוצאות…</div>;
  }

  if (error) {
    return (
      <div className="page-shell" dir="rtl">
        <div className="empty-state">
          אין נתונים על המבחן
          <div>
            <Link to="/dashboard"> ← חזרה לדף הבית</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell" dir="rtl">
      <div className="results-container">
        <div className="results-header">
          <Link className="back-button" to="/dashboard">
            ← חזרה לדף הבית
          </Link>
          <div>
            <p className="eyebrow">תוצאות מבחן</p>
            <h1>{results?.examName ?? '-'}</h1>
            <p>{results?.subject ?? '-'}</p>
          </div>
          <div className="score-pill">ציון: {results?.score ?? '-'}</div>
        </div>

        {results?.questions.map((question, index) => {
          const statusClass = question.isCorrect ? 'correct' : question.score > 0 ? 'partial' : 'wrong';
          return (
            <article key={question.questionId} className={`result-card status-${statusClass}`}>
              <div className="result-card-top">
                <h2>שאלה {index + 1}</h2>
                <span className={`status-badge status-${statusClass}`}>{question.isCorrect ? 'נכון' : question.score > 0 ? 'חלקי' : 'לא נכון'}</span>
              </div>
              <p className="result-question-text">{question.text ?? '-'}</p>
              <div className="result-grid">
                <div>
                  <span>תשובת התלמיד</span>
                  <p>{question.studentAnswer ?? '-'}</p>
                </div>
                <div>
                  <span>התשובה הנכונה</span>
                  <p>{question.correctAnswer ?? '-'}</p>
                </div>
                <div>
                  <span>הניקוד שהתקבל</span>
                  <p>{question.score ?? '-'}</p>
                </div>
                <div>
                  <span>הניקוד המקסימלי</span>
                  <p>{question.maxScore ?? '-'}</p>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
};
