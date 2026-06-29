import type { ClassModel } from "./Class"
import type { Exam } from "./Exam"

export interface ExamClass {
  class_id: number
  exam_id: number
  class_?: ClassModel
  exam?: Exam
}
