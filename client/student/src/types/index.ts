export type ExamStatus = 'Active' | 'InProgress' | 'Submitted' | 'Draft' | 'Closed';
export type QuestionType = 'MCQ' | 'TEXT';
export type QuestionMarkStatus = 'none' | 'in-progress' | 'review';

export interface User {
  studentId: number;
  name: string;
  classId: number;
}

export interface ExamCardModel {
  examId: number;
  name: string;
  subject: string;
  status: ExamStatus;
  durationMinutes: number;
}

export interface QuestionOption {
  optionId: number;
  text: string;
}

export interface QuestionModel {
  questionId: number;
  questionNumber: number;
  text: string;
  type: QuestionType;
  maxScore: number;
  options: QuestionOption[];
}

export interface AnswerValue {
  answerText?: string;
  selectedOptionId?: number;
}

export interface ExamInitialPayload {
  exam: {
    examId: number;
    name: string;
    subject: string;
    durationMinutes: number;
  };
  studentExam: {
    studentExamId: number;
    status: ExamStatus;
    startTime: string;
    endTime: string;
  };
  questions: QuestionModel[];
  answers: Array<{
    questionId: number;
    answerText: string | null;
    selectedOptionId: number | null;
  }>;
  serverTime: string;
}

export interface ResultQuestion {
  questionId: number;
  text: string;
  studentAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  score: number;
  maxScore: number;
}

export interface ResultsPayload {
  examName: string;
  subject: string;
  score: number;
  questions: ResultQuestion[];
}
