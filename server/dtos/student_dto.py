from dataclasses import dataclass


@dataclass
class StudentDTO:
    student_id: int
    first_name: str
    last_name: str
    class_id: int
    is_active: bool