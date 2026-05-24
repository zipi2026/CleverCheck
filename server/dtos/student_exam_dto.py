from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class StudentExamDTO:
    student_exam_id: int
    exam_id: int
    student_id: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    score: Optional[float]