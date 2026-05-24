from dataclasses import dataclass


@dataclass
class QuestionDTO:
    question_id: int
    question_number: int
    exam_id: int
    question_text: str
    question_type_id: int
    max_score: float