import type { Option } from "./Option"
import type { Question } from "./Question"

export interface TeacherAnswer {
  id: number
  question_id: number
  correct_option_id?: number | null
  answer_text?: string | null
  question?: Question
  correct_option?: Option
}
