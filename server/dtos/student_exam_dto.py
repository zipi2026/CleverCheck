import  datetime
class StudentExamDTO:
    def __init__(
        self,
        exam_id: int,
        student_id: int,
        start_time: datetime = None,
        end_time: datetime = None,
        score: float = None
    ):

        if exam_id is None:
            raise ValueError("exam_id is required")

        if student_id is None:
            raise ValueError("student_id is required")

        if score is not None and score < 0:
            raise ValueError("score cannot be negative")

        self.exam_id = exam_id
        self.student_id = student_id
        self.start_time = start_time
        self.end_time = end_time
        self.score = score