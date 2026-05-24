class TeacherDTO:
    def __init__(self, FirstName: str, LastName: str, Email: str, IsActive: bool, Role: str):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.IsActive = IsActive
        self.Role = Role