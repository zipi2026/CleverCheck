import { SERVER_URL } from '../config'

const API_BASE_URL = import.meta.env.DEV ? '' : (SERVER_URL || 'http://localhost:5000')

export interface QuestionResponse {
  id: number
  questionNumber: number
  examID: number
  questionText: string
  questionTypeID: number
  maxScore: number
}

export interface QuestionTypeResponse {
  id: number
  typeName: string
}

export interface OptionResponse {
  id: number
  optionNumber: number
  questionID: number
  optionText: string
}

async function handleJsonResponse<T>(response: Response): Promise<T> {
  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    const message = payload?.message || response.statusText || 'Request failed.'
    throw new Error(String(message))
  }

  return payload as T
}

export async function fetchQuestions(examId?: number): Promise<QuestionResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/questions`)
  const questions = await handleJsonResponse<QuestionResponse[]>(response)

  if (examId === undefined) {
    return questions
  }

  return questions.filter((question) => question.examID === examId)
}

export async function fetchQuestionTypes(): Promise<QuestionTypeResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/question_types`)
  return handleJsonResponse<QuestionTypeResponse[]>(response)
}

export async function fetchOptions(): Promise<OptionResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/options`)
  return handleJsonResponse<OptionResponse[]>(response)
}
