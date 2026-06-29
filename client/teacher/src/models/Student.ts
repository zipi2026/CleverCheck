import type { ClassModel } from "./Class"
import type { StudentExam } from "./StudentExam"

export interface Student {
  id: number
  password_hash: string
  first_name: string
  last_name: string
  class_id: number
  is_active: boolean
  class_?: ClassModel
  student_exams?: StudentExam[]
}
