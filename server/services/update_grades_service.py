class UpdateGradesService:
    def __init__(
        self,
        student_answer_repo,
        question_repo,
        teacher_answer_repo,
        student_exam_repo,
        session
    ):
        # מחברי repositories + session
        self.student_answer_repo = student_answer_repo
        self.question_repo = question_repo
        self.teacher_answer_repo = teacher_answer_repo
        self.student_exam_repo = student_exam_repo
        self.session = session

    def update_exam_grades(self, student_exam_id: int):

        # 1. שליפת כל התשובות של התלמיד למבחן
        answers = self.student_answer_repo.get_by_exam(student_exam_id)

        # משתנה לציון כולל של המבחן
        total_score = 0

        # 2. מעבר על כל תשובה של תלמיד
        for answer in answers:

            # 3. שליפת השאלה הרלוונטית
            question = self.question_repo.get_by_id(answer.question_id)

            # 4. שליפת תשובת המורה (נכון)
            teacher_answer = self.teacher_answer_repo.get_by_question(
                answer.question_id
            )

            # 5. בדיקה האם זו שאלה אמריקאית
            if answer.selected_option_id is not None:

                # 6. בדיקת תשובה אמריקאית
                if answer.selected_option_id == teacher_answer.correct_option_id:
                    score = question.max_score  # תשובה נכונה = מלוא הניקוד
                else:
                    score = 0  # תשובה שגויה = 0

            else:
                # 7. שאלה פתוחה (כרגע מניח שיש כבר ציון קיים או שירות אחר)
                score = answer.score or 0

            # 8. עדכון הציון של התשובה
            answer.score = score

            # 9. הוספה לציון הכולל של המבחן
            total_score += score

        # 10. שליפת המבחן עצמו
        exam = self.student_exam_repo.get_by_id(student_exam_id)

        if exam:
            # 11. עדכון ציון כולל של המבחן
            exam.score = total_score

        # 12. שמירת כל השינויים בבת אחת
        self.session.commit()