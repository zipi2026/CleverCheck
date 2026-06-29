import type { Exam } from "./Exam"
import type { Student } from "./Student"
import type { StudentAnswer } from "./StudentAnswer"

export interface StudentExam {
  id: number
  exam_id: number
  student_id: number
  start_time?: string | null
  end_time?: string | null
  score?: number | null
  exam?: Exam
  student?: Student
  answers?: StudentAnswer[]
}
