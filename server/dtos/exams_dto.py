from datetime import datetime

class ExamDTO:
    def __init__(
        self,
        exam_name: str,
        teacher_id: int,
        subject_id: int,
        start_time: datetime,
        end_time: datetime,
        duration_minutes: int,
        status: str
    ):
        self.exam_name = exam_name
        self.teacher_id = teacher_id
        self.subject_id = subject_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration_minutes = duration_minutes
        self.status = status