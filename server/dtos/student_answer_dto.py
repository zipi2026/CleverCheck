class StudentAnswerDTO:
    def __init__(
        self,
        student_exam_id: int,
        question_id: int,
        answer_text: str = None,
        selected_option_id: int = None,
        score: float = None
    ):
        self.student_exam_id = student_exam_id
        self.question_id = question_id
        self.answer_text = answer_text
        self.selected_option_id = selected_option_id
        self.score = score
