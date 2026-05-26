class StudentAnswerDTO:
    def __init__(
        self,
        StudentExamID: int,
        QuestionID: int,
        AnswerText: str = None,
        SelectedOptionID: int = None,
        Score: float = None
    ):
        self.StudentExamID = StudentExamID
        self.QuestionID = QuestionID
        self.AnswerText = AnswerText
        self.SelectedOptionID = SelectedOptionID
        self.Score = Score