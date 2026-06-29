import { useEffect, useMemo, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { examService } from '../services/examService';
import { useAuthStore } from '../store/authStore';
import type { ExamCardModel } from '../types';

const getStatusMeta = (status: ExamCardModel['status']) => {
  switch (status) {
    case 'Active':
      return { label: 'פעיל', tone: 'active', description: 'זמין כעת למענה' };
    case 'InProgress':
      return { label: 'בתהליך', tone: 'in-progress', description: 'התחלת לענות' };
    case 'Submitted':
      return { label: 'ממתין לבדיקה', tone: 'submitted', description: 'ההגשה נקלטה' };
    case 'Draft':
      return { label: 'הוגש עם ציון', tone: 'Draft', description: 'הציון זמין' };
    default:
      return { label: 'לא זמין', tone: 'closed', description: 'הבחינה סגורה או לא זמינה עדיין' };
  }
};

export const DashboardPage = () => {
  const isAuthenticated = useAuthStore((state: { isAuthenticated: boolean }) => state.isAuthenticated);
  const loading = useAuthStore((state: { loading: boolean }) => state.loading);
  const user = useAuthStore((state: { user: { studentId: number; name: string; classId: number } | null }) => state.user);
  const [exams, setExams] = useState<ExamCardModel[]>([]);
  const [search, setSearch] = useState('');
  const [subject, setSubject] = useState('הכל');
  console.log("Dashboard mounted");
  useEffect(() => {
  console.log("calling listExams");

  examService.listExams()
    .then((data) => {
      console.log("EXAMS RECEIVED:", data);
      setExams(data);
    })
    .catch((err) => {
      console.error("LIST EXAMS FAILED:", err);
    });
}, []);

  const subjects = useMemo(() => ['הכל', ...Array.from(new Set(exams.map((exam) => exam.subject)))], [exams]);
  const filteredExams = useMemo(() => {
    return exams.filter((exam) => {
      const matchesSearch = `${exam.name} ${exam.subject}`.toLowerCase().includes(search.trim().toLowerCase());
      const matchesSubject = subject === 'הכל' || exam.subject === subject;
      return matchesSearch && matchesSubject;
    });
  }, [exams, search, subject]);

  const activeExams = filteredExams.filter((exam) => exam.status === 'Active' || exam.status === 'InProgress');
  const upcomingExams = filteredExams.filter((exam) => exam.status === 'Closed');
  const completedExams = filteredExams.filter((exam) => exam.status === 'Submitted' || exam.status === 'Draft');

  const getActionState = (exam: ExamCardModel) => {
    if (exam.status === 'Active') {
      return { label: 'התחל מבחן', enabled: true, to: `/exam/${exam.examId}` };
    }
    if (exam.status === 'InProgress') {
      return { label: 'המשך מבחן', enabled: true, to: `/exam/${exam.examId}` };
    }
    if (exam.status === 'Draft') {
      return { label: 'צפייה בתוצאות', enabled: true, to: `/results/${exam.examId}` };
    }
    if (exam.status === 'Submitted') {
      return { label: 'בבדיקה', enabled: false, to: '#' };
    }
    return { label: 'עדיין לא זמין', enabled: false, to: '#' };
  };

  if (loading) {
    return <div className="page-loading">בודק כניסה…</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="page-shell" dir="rtl">
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">מערכת מבחנים</p>
            <h1>שלום, {user?.name ?? 'סטודנט'}</h1>
            <p>היכנס למבחנים הזמינים, המשך במבחנים בעבודה וצפה בתוצאות.</p>
          </div>
          <div className="dashboard-toolbar">
            <input
              aria-label="חיפוש מבחן"
              className="search-input"
              placeholder="חיפוש מבחן"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <select aria-label="סינון לפי מקצוע" className="filter-select" value={subject} onChange={(event) => setSubject(event.target.value)}>
              {subjects.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
        </header>

        <section className="dashboard-section">
          <div className="section-title-row">
            <div>
              <h2>מבחנים פעילים</h2>
              <p>מבחנים פתוחים כרגע למענה</p>
            </div>
            <span className="section-count">{activeExams.length}</span>
          </div>
          {activeExams.length ? (
            <div className="exam-list">
              {activeExams.map((exam) => {
                const meta = getStatusMeta(exam.status);
                const action = getActionState(exam);
                return (
                  <article key={exam.examId} className="exam-card">
                    <div className="exam-card-top">
                      <div>
                        <h3>{exam.name}</h3>
                        <p>{exam.subject}</p>
                      </div>
                      <span className={`status-badge status-${meta.tone}`}>{meta.label}</span>
                    </div>
                    <div className="exam-card-meta">
                      <div>
                        <span>משך</span>
                        <strong>{exam.durationMinutes} דקות</strong>
                      </div>
                      <div>
                        <span>זמן פנוי</span>
                        <strong>{exam.durationMinutes} דקות</strong>
                      </div>
                    </div>
                    <div className="exam-card-footer">
                      {action.enabled ? (
                        <Link className="primary-button" to={action.to}>
                          {action.label}
                        </Link>
                      ) : (
                        <button className="secondary-button" disabled>
                          {action.label}
                        </button>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">אין מבחנים פעילים כרגע.</div>
          )}
        </section>

        <section className="dashboard-section">
          <div className="section-title-row">
            <div>
              <h2>מבחנים עתידיים</h2>
              <p>מבחנים שטרם נפתחים</p>
            </div>
            <span className="section-count">{upcomingExams.length}</span>
          </div>
          {upcomingExams.length ? (
            <div className="exam-list">
              {upcomingExams.map((exam) => {
                const meta = getStatusMeta(exam.status);
                return (
                  <article key={exam.examId} className="exam-card">
                    <div className="exam-card-top">
                      <div>
                        <h3>{exam.name}</h3>
                        <p>{exam.subject}</p>
                      </div>
                      <span className={`status-badge status-${meta.tone}`}>{meta.label}</span>
                    </div>
                    <div className="exam-card-footer">
                      <button className="secondary-button" disabled>
                        עדיין לא זמין
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">אין מבחנים עתידיים להצגה.</div>
          )}
        </section>

        <section className="dashboard-section">
          <div className="section-title-row">
            <div>
              <h2>מבחנים שהושלמו</h2>
              <p>מבחנים שכבר נענו וניתן לצפות בתוצאות</p>
            </div>
            <span className="section-count">{completedExams.length}</span>
          </div>
          {completedExams.length ? (
            <div className="exam-list">
              {completedExams.map((exam) => {
                const meta = getStatusMeta(exam.status);
                const action = getActionState(exam);
                return (
                  <article key={exam.examId} className="exam-card">
                    <div className="exam-card-top">
                      <div>
                        <h3>{exam.name}</h3>
                        <p>{exam.subject}</p>
                      </div>
                      <span className={`status-badge status-${meta.tone}`}>{meta.label}</span>
                    </div>
                    <div className="exam-card-meta">
                      <div>
                        <span>משך</span>
                        <strong>{exam.durationMinutes} דקות</strong>
                      </div>
                    </div>
                    <div className="exam-card-footer">
                      {action.enabled ? (
                        <Link className="primary-button" to={action.to}>
                          {action.label}
                        </Link>
                      ) : (
                        <button className="secondary-button" disabled>
                          {action.label}
                        </button>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">עדיין לא הושלמו מבחנים.</div>
          )}
        </section>
      </div>
    </div>
  );
};
