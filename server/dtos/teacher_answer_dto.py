class TeacherAnswerDTO:
    def __init__(self, question_id: int, answer_text: str = None, correct_option_id: int = None):
        self.question_id = question_id
        self.answer_text = answer_text
        self.correct_option_id = correct_option_id