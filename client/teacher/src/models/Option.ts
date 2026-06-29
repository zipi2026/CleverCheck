import type { Question } from "./Question"

export interface Option {
  id: number
  option_number: number
  question_id: number
  option_text: string
  question?: Question
}
