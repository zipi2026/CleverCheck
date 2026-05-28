class QuestionDTO:
    def __init__(
        self,
        question_number: int,
        exam_id: int,
        question_text: str,
        question_type_id: int,
        max_score: float
    ):
        self.question_number = question_number
        self.exam_id = exam_id
        self.question_text = question_text
        self.question_type_id = question_type_id
        self.max_score = max_score