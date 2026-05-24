class QuestionDTO:
    def __init__(
        self,
        QuestionNumber: int,
        ExamID: int,
        QuestionText: str,
        QuestionTypeID: int,
        MaxScore: float
    ):
        self.QuestionNumber = QuestionNumber
        self.ExamID = ExamID
        self.QuestionText = QuestionText
        self.QuestionTypeID = QuestionTypeID
        self.MaxScore = MaxScore
