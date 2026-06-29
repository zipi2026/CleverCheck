import type { Exam } from "./Exam"
import type { TeacherClass } from "./TeacherClass"

export interface Teacher {
  id: number
  password_hash: string
  first_name: string
  last_name: string
  email: string
  is_active: boolean
  role: string
  exams?: Exam[]
  teacher_classes?: TeacherClass[]
}

