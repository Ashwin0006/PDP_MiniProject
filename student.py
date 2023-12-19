# Object representation of the student.

class Student:
    def __init__(self, name, pwd, id, personal, mentor_assigned=None):
        self.name = name
        self._pwd = pwd
        self.id = id
        self.personal = personal
        self.mentor_assigned = mentor_assigned
        self.role = 'student'