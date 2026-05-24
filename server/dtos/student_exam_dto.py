from datetime import datetime


class StudentExamDTO:
    def __init__(
        self,
        ExamID: int,
        StudentID: int,
        StartTime: datetime = None,
        EndTime: datetime = None,
        Score: float = None
    ):
        self.ExamID = ExamID
        self.StudentID = StudentID
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Score = Score