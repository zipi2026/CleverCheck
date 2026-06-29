import type { Exam } from "./Exam"
import type { Option } from "./Option"
import type { QuestionType } from "./QuestionType"
import type { StudentAnswer } from "./StudentAnswer"
import type { TeacherAnswer } from "./TeacherAnswer"

export interface Question {
  id: number
  question_number: number
  exam_id: number
  question_text: string
  question_type_id: number
  max_score: number
  exam?: Exam
  question_type?: QuestionType
  options?: Option[]
  teacher_answer?: TeacherAnswer
  student_answers?: StudentAnswer[]
}
