from datetime import datetime


class ExamDTO:
    def __init__(
        self,
        ExamName: str,
        TeacherID: int,
        SubjectID: int,
        StartTime: datetime,
        EndTime: datetime,
        DurationMinutes: int,
        Status: str
    ):
        self.ExamName = ExamName
        self.TeacherID = TeacherID
        self.SubjectID = SubjectID
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.DurationMinutes = DurationMinutes
        self.Status = Status