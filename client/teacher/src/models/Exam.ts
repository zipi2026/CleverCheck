import type { ExamClass } from "./ExamClass"
import type { Question } from "./Question"
import type { StudentExam } from "./StudentExam"
import type { Subject } from "./Subject"
import type { Teacher } from "./Teacher"

export interface Exam {
  id: number
  exam_name: string
  teacher_id: number
  subject_id: number
  start_time: string
  end_time: string
  duration_minutes: number
  created_at?: string | null
  status: string
  teacher?: Teacher
  subject?: Subject
  questions?: Question[]
  student_exams?: StudentExam[]
  exam_classes?: ExamClass[]
}
