import { create } from 'zustand';
import type { AnswerValue, QuestionMarkStatus } from '../types';

export type ExamPageStatus = 'idle' | 'active' | 'submitted';

type ExamStore = {
  exam: any | null;
  studentExam: any | null;
  questions: any[];
  answers: Record<number, AnswerValue>;
  currentQuestion: number;
  markedQuestions: number[];
  inProgressQuestions: number[];
  visitedQuestions: number[];
  status: ExamPageStatus;
  setExamData: (payload: any) => void;
  setAnswer: (questionId: number, value: AnswerValue) => void;
  setCurrentQuestion: (id: number) => void;
  setQuestionStatus: (id: number, status: QuestionMarkStatus) => void;
  setStatus: (status: ExamPageStatus) => void;
  reset: () => void;
};

const initialState = {
  exam: null,
  studentExam: null,
  questions: [],
  answers: {},
  currentQuestion: 0,
  markedQuestions: [] as number[],
  inProgressQuestions: [] as number[],
  visitedQuestions: [] as number[],
  status: 'idle' as ExamPageStatus,
};



export const useExamStore = create<ExamStore>((set: (partial: Partial<ExamStore> | ((state: ExamStore) => Partial<ExamStore>)) => void) => ({
  ...initialState,
  setExamData: (payload: any) =>
    set((state: ExamStore) => ({
      exam: payload.exam,
      studentExam: payload.studentExam,
      questions: payload.questions,
      answers: Object.fromEntries(
        (payload.answers || []).map((answer: any) => [answer.questionId, { answerText: answer.answerText ?? undefined, selectedOptionId: answer.selectedOptionId ?? undefined }]),
      ),
      currentQuestion: payload.currentQuestion ?? (state.currentQuestion || 0),
      markedQuestions: payload.markedQuestions ?? state.markedQuestions,
      inProgressQuestions: payload.inProgressQuestions ?? state.inProgressQuestions,
      visitedQuestions: payload.visitedQuestions ?? state.visitedQuestions,
      status: payload.studentExam?.status === 'Submitted' || payload.studentExam?.status === 'Graded' ? 'submitted' : 'active',
    })),
  setAnswer: (questionId: number, value: AnswerValue) =>
    set((state: ExamStore) => ({
      answers: { ...state.answers, [questionId]: value },
      visitedQuestions: state.visitedQuestions.includes(questionId) ? state.visitedQuestions : [...state.visitedQuestions, questionId],
    })),
  setCurrentQuestion: (id: number) =>
    set((state: ExamStore) => {
      const questionId = state.questions[id]?.questionId ?? id;
      return {
        currentQuestion: id,
        visitedQuestions: state.visitedQuestions.includes(questionId) ? state.visitedQuestions : [...state.visitedQuestions, questionId],
      };
    }),
  setQuestionStatus: (id: number, status: QuestionMarkStatus) =>
    set((state: ExamStore) => {
      const reviewQuestions = state.markedQuestions.filter((questionId) => questionId !== id);
      const inProgressQuestions = state.inProgressQuestions.filter((questionId) => questionId !== id);

      if (status === 'review') {
        return { markedQuestions: [...reviewQuestions, id], inProgressQuestions };
      }

      if (status === 'in-progress') {
        return { markedQuestions: reviewQuestions, inProgressQuestions: [...inProgressQuestions, id] };
      }

      return { markedQuestions: reviewQuestions, inProgressQuestions };
    }),
  setStatus: (status: ExamPageStatus) => set({ status }),
  reset: () => set(initialState),
}));
