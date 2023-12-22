import pickle
import types



class Report:
    def __init__(self, strategy=None):
        if(strategy is not None):
            self.strategy = strategy
            self.strategy_method = types.MethodType(strategy)
        else:
            # Default one!
            self.strategy = "Complete_Details"
    
    def generate(self):
        data = self.strategy_method()
        return data
    
    def strategy_method(self):
        data = Complete_Details()
        return data
    
    def change_stratergy(self, strategy):
        self.strategy = strategy
        self.strategy_method = types.MethodType(strategy)


# Stratergy 1
def Complete_Details():
    # Define a helper Method
    def get_full_detail(obj, req_data):
        data = None
        for k,v in req_data.items():
            for stud_obj in v:
                if(stud_obj.name == obj.name and stud_obj.id == obj.id and stud_obj._pwd == obj._pwd):
                    mentor = k.name
                    student_name = obj.name
                    student_details = obj.personal
                    data = "-" * 40 + "\n" + f"Student Name :{student_name}\nStudent Id :{obj.id}\nMentor Name :{mentor}\nDetails :{student_details}\n" 

        return data

    with open('student_data.pickle', 'rb' ) as infile:
        student_data = pickle.load(infile)

    with open('mentor_mentee.pickle', 'rb' ) as infile:
        mentor_mentee_data = pickle.load(infile)

    print(student_data)
    print(mentor_mentee_data)

    # Generating Report
    reports_data = ""
    for student_obj in student_data:
        reports_data += get_full_detail(student_obj, mentor_mentee_data)
    
    return reports_data

if __name__ == "__main__":
    r1 = Report()
    # Using Statergy 1
    print(r1.generate())