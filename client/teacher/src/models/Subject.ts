import type { Exam } from "./Exam"

export interface Subject {
  subject_id: number
  subject_name: string
  exams?: Exam[]
}
