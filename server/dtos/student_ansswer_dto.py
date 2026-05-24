from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentAnswerDTO:
    answer_id: int
    student_exam_id: int
    question_id: int
    answer_text: Optional[str]
    selected_option_id: Optional[int]
    score: Optional[float]