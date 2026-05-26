class TeacherAnswerDTO:
    def __init__(self, QuestionID: int, AnswerText: str = None, CorrectOptionID: int = None):
        self.QuestionID = QuestionID
        self.AnswerText = AnswerText
        self.CorrectOptionID = CorrectOptionID