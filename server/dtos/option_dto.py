class OptionDTO:
    def __init__(self, option_number: int, question_id: int, option_text: str):
        self.option_number = option_number
        self.question_id = question_id
        self.option_text = option_text