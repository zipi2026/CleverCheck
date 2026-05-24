from dataclasses import dataclass


@dataclass
class QuestionTypeDTO:
    question_type_id: int
    type_name: str