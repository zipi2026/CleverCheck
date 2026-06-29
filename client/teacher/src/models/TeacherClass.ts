import type { ClassModel } from "./Class"
import type { Teacher } from "./Teacher"

export interface TeacherClass {
  teacher_id: number
  class_id: number
  teacher?: Teacher
  class_?: ClassModel
}
