from dataclasses import dataclass


@dataclass
class TeacherDTO:
    teacher_id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    role: str