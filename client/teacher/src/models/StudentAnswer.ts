import type { Option } from "./Option"
import type { Question } from "./Question"
import type { StudentExam } from "./StudentExam"

export interface StudentAnswer {
  id: number
  student_exam_id: number
  question_id: number
  selected_option_id?: number | null
  answer_text?: string | null
  score?: number | null
  student_exam?: StudentExam
  question?: Question
  option?: Option
}
