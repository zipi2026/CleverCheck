import type { Question } from "./Question"

export interface QuestionType {
  id: number
  type_name: string
  questions?: Question[]
}
