import type { ExamClass } from "./ExamClass"
import type { Student } from "./Student"
import type { TeacherClass } from "./TeacherClass"

export interface ClassModel {
  id: number
  class_name: string
  students?: Student[]
  exam_classes?: ExamClass[]
  teacher_classes?: TeacherClass[]
}
