import type { ExamCardModel, ExamInitialPayload, ExamStatus, ResultsPayload } from '../types';

const API_BASE = 'http://localhost:5000/api';

const parseJson = async (response: Response) => {
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const message = payload?.error || payload?.message || response.statusText || 'Request failed';
    throw new Error(String(message));
  }
  return payload;
};

export const examService = {
  listExams: async (): Promise<ExamCardModel[]> => {
    const payload = await parseJson(await fetch(`${API_BASE}/exams`, { credentials: 'include' }));
    console.log("EXAMS FROM SERVER:", payload);
    return (payload as Array<{ id: number; examName: string; subjectID: string; status: string; durationMinutes: number }>).map((exam) => ({
      examId: exam.id,
      name: exam.examName,
      subject: exam.subjectID,
      status: exam.status as ExamStatus,
      durationMinutes: exam.durationMinutes,
}));
  },
  getExam: async (examId: string): Promise<ExamInitialPayload> => {
    const payload = await parseJson(await fetch(`${API_BASE}/student_exams/exam/${examId}`, { credentials: 'include' }));
    return payload as ExamInitialPayload;
  },
  saveAnswer: async (payload: { studentExamId: number; questionId: number; answerText: string | null; selectedOptionId: number | null }) => {
    const response = await fetch(`${API_BASE}/exams/${payload.studentExamId / 100}/answers`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return parseJson(response);
  },
  submitExam: async (studentExamId: number) => {
    const response = await fetch(`${API_BASE}/exams/${studentExamId / 100}/submit`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ studentExamId }),
    });
    return parseJson(response);
  },
  getResults: async (studentExamId: string): Promise<ResultsPayload> => {
    const response = await fetch(`${API_BASE}/student_exams/${Number(studentExamId) / 100}/results`, { credentials: 'include' });
    const payload = await parseJson(response);
    return payload as ResultsPayload;
  },
};
