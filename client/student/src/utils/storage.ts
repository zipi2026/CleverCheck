const STORAGE_KEYS = {
  answers: 'answers',
  currentQuestion: 'currentQuestion',
  markedQuestions: 'markedQuestions',
  inProgressQuestions: 'inProgressQuestions',
  visitedQuestions: 'visitedQuestions',
  lastSavedAt: 'lastSavedAt',
};

export const saveExamUiState = (
  studentExamId: number,
  answers: Record<number, { answerText?: string; selectedOptionId?: number }>,
  currentQuestion: number,
  markedQuestions: number[],
  visitedQuestions: number[],
  inProgressQuestions: number[],
) => {
  const payload = {
    studentExamId,
    answers,
    currentQuestion,
    markedQuestions,
    visitedQuestions,
    inProgressQuestions,
    lastSavedAt: new Date().toISOString(),
  };

  localStorage.setItem(STORAGE_KEYS.answers, JSON.stringify(payload.answers));
  localStorage.setItem(STORAGE_KEYS.currentQuestion, String(payload.currentQuestion));
  localStorage.setItem(STORAGE_KEYS.markedQuestions, JSON.stringify(payload.markedQuestions));
  localStorage.setItem(STORAGE_KEYS.inProgressQuestions, JSON.stringify(payload.inProgressQuestions));
  localStorage.setItem(STORAGE_KEYS.visitedQuestions, JSON.stringify(payload.visitedQuestions));
  localStorage.setItem(STORAGE_KEYS.lastSavedAt, payload.lastSavedAt);
};

export const loadExamUiState = () => {
  const answersRaw = localStorage.getItem(STORAGE_KEYS.answers);
  const currentQuestionRaw = localStorage.getItem(STORAGE_KEYS.currentQuestion);
  const markedQuestionsRaw = localStorage.getItem(STORAGE_KEYS.markedQuestions);
  const inProgressQuestionsRaw = localStorage.getItem(STORAGE_KEYS.inProgressQuestions);
  const visitedQuestionsRaw = localStorage.getItem(STORAGE_KEYS.visitedQuestions);
  const lastSavedAtRaw = localStorage.getItem(STORAGE_KEYS.lastSavedAt);

  return {
    answers: answersRaw ? JSON.parse(answersRaw) : {},
    currentQuestion: currentQuestionRaw ? Number(currentQuestionRaw) : 0,
    markedQuestions: markedQuestionsRaw ? JSON.parse(markedQuestionsRaw) : [],
    inProgressQuestions: inProgressQuestionsRaw ? JSON.parse(inProgressQuestionsRaw) : [],
    visitedQuestions: visitedQuestionsRaw ? JSON.parse(visitedQuestionsRaw) : [],
    lastSavedAt: lastSavedAtRaw ?? null,
  };
};
