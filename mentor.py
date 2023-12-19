#Object representation of the mentor

class Mentor:
    def __init__(self, name, pwd, id, details:list):
        self.name = name
        self._pwd = pwd
        self.id = id
        self.details = details
        self.role = "mentor"
    
    