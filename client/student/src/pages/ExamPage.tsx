import { useEffect, useMemo, useRef, useState } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import { examService } from '../services/examService';
import { useAuthStore } from '../store/authStore';
import { useExamStore } from '../store/examStore';
import { useUIStore } from '../store/uiStore';
import type { AnswerValue, QuestionMarkStatus } from '../types';
import { loadExamUiState, saveExamUiState } from '../utils/storage';

const formatTime = (ms: number) => {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
};

const getQuestionBadge = (questionId: number, answers: Record<number, AnswerValue>, markedQuestions: number[], inProgressQuestions: number[], index: number, currentQuestion: number) => {
  if (markedQuestions.includes(questionId)) {
    return { label: 'לבדיקה', tone: 'review' };
  }
  if (inProgressQuestions.includes(questionId)) {
    return { label: 'בעבודה', tone: 'in-progress' };
  }
  if (index === currentQuestion) {
    return { label: 'נוכחי', tone: 'current' };
  }
  if (answers[questionId] && (answers[questionId].answerText || answers[questionId].selectedOptionId !== undefined)) {
    return { label: 'נענה', tone: 'answered' };
  }
  return { label: 'לא נענה', tone: 'unanswered' };
};

export const ExamPage = () => {
  const { examId } = useParams();
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state: { isAuthenticated: boolean }) => state.isAuthenticated);
  const loadingAuth = useAuthStore((state: { loading: boolean }) => state.loading);
  const { exam, questions, answers, currentQuestion, markedQuestions, inProgressQuestions, setExamData, setAnswer, setCurrentQuestion, setQuestionStatus, setStatus, reset } = useExamStore();
  const { timerVisible, sidebarOpen, setTimerVisible, setSidebarOpen } = useUIStore();
  const [remainingMs, setRemainingMs] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [recovered, setRecovered] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [showFinalConfirm, setShowFinalConfirm] = useState(false);
  const questionRefs = useRef<Array<HTMLElement | null>>([]);

  useEffect(() => {
    const loadExam = async () => {
      setLoading(true);
      const payload = await examService.getExam(examId ?? '1');
      const recoveredState = loadExamUiState();
      const mergedAnswers = {
        ...payload.answers.reduce((acc: Record<number, AnswerValue>, answer: any) => ({ ...acc, [answer.questionId]: { answerText: answer.answerText ?? undefined, selectedOptionId: answer.selectedOptionId ?? undefined } }), {}),
        ...recoveredState.answers,
      };
      const mergedPayload = {
        ...payload,
        answers: Object.entries(mergedAnswers).map(([questionId, value]) => ({
          questionId: Number(questionId),
          answerText: (value as AnswerValue).answerText ?? null,
          selectedOptionId: (value as AnswerValue).selectedOptionId ?? null,
        })),
        currentQuestion: recoveredState.currentQuestion ?? 0,
        markedQuestions: recoveredState.markedQuestions ?? [],
        inProgressQuestions: recoveredState.inProgressQuestions ?? [],
        visitedQuestions: recoveredState.visitedQuestions ?? [],
      };
      setExamData(mergedPayload);
      setRemainingMs(new Date(payload.studentExam.endTime).getTime() - new Date(payload.serverTime).getTime());
      setRecovered(true);
      setLoading(false);
    };

    void loadExam();
    return () => {
      reset();
    };
  }, [examId, reset, setExamData]);

  useEffect(() => {
    if (!recovered || remainingMs <= 0) {
      return;
    }
    const interval = window.setInterval(() => {
      setRemainingMs((value) => value - 1000);
    }, 1000);
    return () => window.clearInterval(interval);
  }, [recovered, remainingMs]);

  useEffect(() => {
    if (recovered && remainingMs <= 0 && !submitting) {
      void handleSubmit();
    }
  }, [recovered, remainingMs, submitting]);

  const handleSubmit = async () => {
    if (submitting) return;
    setSubmitting(true);
    const studentExamId = Number(exam?.examId ?? 0) * 100;
    try {
      await examService.submitExam(studentExamId);
      setStatus('submitted');
      navigate('/dashboard', { replace: true });
    } catch {
      // keep local state and retry later
    } finally {
      setSubmitting(false);
    }
  };

  const persistExamState = () => {
    const state = useExamStore.getState();
    const studentExamId = Number(exam?.examId ?? 0) * 100;
    saveExamUiState(studentExamId, state.answers, state.currentQuestion, state.markedQuestions, state.visitedQuestions, state.inProgressQuestions);
  };

  const jumpToQuestion = (index: number) => {
    setCurrentQuestion(index);
    window.setTimeout(() => {
      questionRefs.current[index]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 0);
    persistExamState();
  };

  const currentQuestionData = questions[currentQuestion];
  const answeredCount = useMemo(() => Object.values(answers).filter((value) => Boolean(value.answerText) || value.selectedOptionId !== undefined).length, [answers]);
  const unansweredCount = useMemo(() => questions.length - answeredCount, [answers, questions.length]);
  const markedCount = markedQuestions.length;
  const inProgressCount = inProgressQuestions.length;
  
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        event.preventDefault();
        jumpToQuestion(Math.min(questions.length - 1, currentQuestion + 1));
      }
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        event.preventDefault();
        jumpToQuestion(Math.max(0, currentQuestion - 1));
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [currentQuestion, questions.length]);

  if (loadingAuth) {
    return <div className="page-loading">בודק כניסה…</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (loading) {
    return <div className="page-loading">טוען מבחן…</div>;
  }

  if (!currentQuestionData) {
    return <div className="page-loading">המבחן לא נמצא.</div>;
  }

  const updateAnswer = async (questionId: number, value: AnswerValue) => {
    setAnswer(questionId, value);
    const studentExamId = Number(exam?.examId ?? 0) * 100;
    await examService.saveAnswer({
      studentExamId,
      questionId,
      answerText: value.answerText ?? null,
      selectedOptionId: value.selectedOptionId ?? null,
    });
    persistExamState();
  };

  const toggleQuestionStatus = (questionId: number, status: QuestionMarkStatus) => {
    setQuestionStatus(questionId, status);
    persistExamState();
  };

  return (
    <div className="page-shell" dir="rtl">
      <div className="exam-shell">
        <aside className="exam-side-panel left-panel">
          <div className="panel-card">
            <button className="ghost-button" onClick={() => setTimerVisible(!timerVisible)}>
              {timerVisible ? 'הסתר שעון' : 'הצג שעון'}
            </button>
            <button className="ghost-button" onClick={() => setSidebarOpen(!sidebarOpen)}>
              {sidebarOpen ? 'הסתר ניווט' : 'הצג ניווט'}
            </button>
            <button className="primary-button" onClick={() => setShowConfirm(true)} disabled={submitting}>
              {submitting ? 'מגיש…' : 'הגש מבחן'}
            </button>
            <button className="ghost-button" onClick={() => navigate('/dashboard')}>
              חזרה לדף הבית
            </button>
          </div>
          <div className="panel-card sticky-card">
            {timerVisible ? (
              <>
                <p className="eyebrow">זמן שנותר</p>
                <div className="timer-value">{formatTime(remainingMs)}</div>
              </>
            ) : null}
            <div className="stats-grid">
              <div>
                <strong>{answeredCount}</strong>
                <span>ענו</span>
              </div>
              <div>
                <strong>{unansweredCount}</strong>
                <span>לא ענו</span>
              </div>
              <div>
                <strong>{markedCount}</strong>
                <span>לבדיקה</span>
              </div>
              <div>
                <strong>{inProgressCount}</strong>
                <span>בעבודה</span>
              </div>
            </div>
          </div>
        </aside>

        <main className="exam-main-panel">
          <div className="panel-card exam-header-card">
            <div>
              <p className="eyebrow">מבחן</p>
              <h1>{exam?.name}</h1>
              <p>{exam?.subject}</p>
            </div>
            <div className="exam-progress-pill">
              <span>{questions.length} שאלות</span>
              <strong>{answeredCount}/{questions.length} הושלמו</strong>
            </div>
          </div>

          <div className="question-list">
            {questions.map((question: any, index: number) => {
              const status = getQuestionBadge(question.questionId, answers, markedQuestions, inProgressQuestions, index, currentQuestion);
              const questionAnswer = answers[question.questionId] ?? {};
              return (
                <section
                  key={question.questionId}
                  ref={(element) => {
                    questionRefs.current[index] = element;
                  }}
                  className={`question-card ${index === currentQuestion ? 'is-current' : ''}`}
                >
                  <div className="question-card-top">
                    <div className="question-title-row">
                      <span className="question-number">שאלה {question.questionNumber}</span>
                      <span className={`status-badge status-${status.tone}`}>{status.label}</span>
                    </div>
                    <div className="question-meta">
                      <span>ניקוד מקסימלי: {question.maxScore}</span>
                      <span>{question.type === 'MCQ' ? 'שאלה רב-ברירית' : 'שאלה פתוחה'}</span>
                    </div>
                  </div>
                  <h3>{question.text}</h3>
                  {question.type === 'MCQ' ? (
                    <div className="options-list">
                      {question.options.map((option: any) => (
                        <label key={option.optionId} className="option-row">
                          <input
                            type="radio"
                            name={`q-${question.questionId}`}
                            checked={questionAnswer.selectedOptionId === option.optionId}
                            onChange={() => void setAnswer(question.questionId, { selectedOptionId: option.optionId })}
                          />
                          <span>{option.text}</span>
                        </label>
                      ))}
                    </div>
                  ) : (
                    <textarea
                      className="open-answer-input"
                      value={questionAnswer.answerText ?? ''}
                      onChange={(event) => void setAnswer(question.questionId, { answerText: event.target.value })}
                      placeholder="הקלידו תשובה מפורטת…"
                    />
                  )}
                  <div className="question-actions">
                    <button className="ghost-button" onClick={() => jumpToQuestion(index)}>
                      מעבר לשאלה
                    </button>
                    <div className="status-actions">
                      <button className="ghost-button" onClick={() => toggleQuestionStatus(question.questionId, 'in-progress')}>
                        בעבודה
                      </button>
                      <button className="ghost-button" onClick={() => toggleQuestionStatus(question.questionId, 'review')}>
                        לבדיקה
                      </button>
                      <button className="ghost-button" onClick={() => toggleQuestionStatus(question.questionId, 'none')}>
                        נקה סימון
                      </button>
                    </div>
                  </div>
                </section>
              );
            })}
          </div>

          <div className="question-nav-row">
            <button className="ghost-button" onClick={() => jumpToQuestion(Math.max(0, currentQuestion - 1))}>
              לשאלה הקודמת
            </button>
            <button className="ghost-button" onClick={() => jumpToQuestion(Math.min(questions.length - 1, currentQuestion + 1))}>
              לשאלה הבאה
            </button>
          </div>
        </main>

        {sidebarOpen ? (
          <aside className="exam-side-panel right-panel">
            <div className="panel-card">
              <h2>ניווט בין שאלות</h2>
              <div className="navigator-grid">
                {questions.map((question: any, index: number) => {
                  const status = getQuestionBadge(question.questionId, answers, markedQuestions, inProgressQuestions, index, currentQuestion);
                  return (
                    <button key={question.questionId} className={`nav-button status-${status.tone}`} onClick={() => jumpToQuestion(index)}>
                      <span className="nav-question-label">שאלה {question.questionNumber}</span>
                      <span className="nav-status-label">{status.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </aside>
        ) : null}
      </div>

      {showConfirm ? (
        <div className="modal-backdrop" role="dialog" aria-modal="true">
          <div className="modal-card">
            <h2>האם להגיש את המבחן?</h2>
            <p>מספר שאלות שנענו: {answeredCount}</p>
            <p>מספר שאלות שלא נענו: {unansweredCount}</p>
            <div className="modal-actions">
              <button className="ghost-button" onClick={() => setShowConfirm(false)}>
                חזרה למבחן
              </button>
              <button className="primary-button" onClick={() => { setShowConfirm(false); setShowFinalConfirm(true); }}>
                המשך להגשה
              </button>
            </div>
          </div>
        </div>
      ) : null}

      {showFinalConfirm ? (
        <div className="modal-backdrop" role="dialog" aria-modal="true">
          <div className="modal-card">
            <h2>אישור סופי</h2>
            <p>לאחר ההגשה לא ניתן יהיה לחזור למבחן או לשנות תשובות.</p>
            <div className="modal-actions">
              <button className="ghost-button" onClick={() => setShowFinalConfirm(false)}>
                ביטול
              </button>
              <button className="primary-button" onClick={() => void handleSubmit()}>
                הגש סופית
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
