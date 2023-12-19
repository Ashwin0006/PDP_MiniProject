from flask import Flask, render_template, request
import pickle
from student import *
from mentor import *



app = Flask(__name__)
notifications = []
# with open('notifications.pickle', 'rb') as infile:
#     notifications = pickle.load(infile)
#     print(notifications)
def get_details(name):
    pass

def load_from_pickle(path):
    try:
        with open(path, 'rb') as outfile:
            data = pickle.load(outfile)
    except:
        data = Mentor('admin', 'admin', '#123', ['Hello', 'Works as Mentor'])
        write_to_pickle(path, data)
    return data

def write_to_pickle(data, path):
    with open(path, 'rb') as infile:
        lst_data = pickle.load(infile)
    
    lst_data.append(data)

    with open(path, 'wb') as outfile:
        pickle.dump(lst_data, outfile)

def calculate_mentees():
    mentor_data = load_from_pickle("mentor_data.pickle")
    mentee_data = load_from_pickle('student_data.pickle')

    # mentors = []
    # mentees = []
    # for mentor in mentor_data:
    #     mentors.append(mentor)
    # for mentee in mentee_data:
    #     mentees.append(mentee)
    
    pair_dict = {}
    val = []
    for mentor in mentor_data:
        pair_dict[mentor] = val
    
    # Assign then mentor and students pair
    i = 0
    j = 0
    while(j < len(mentee_data)):
        pair_dict[mentor_data[i]].append(mentee_data[j])
        j += 1
        i += 1
        i = i % len(mentor_data)

    final_data = pair_dict
    print(final_data)
    with open('mentor_mentee.pickle', 'wb') as outfile:
        pickle.dump(final_data, outfile)

def check_credentials(name, pwd, role):
    if role == "mentor":
        data = load_from_pickle('mentor_data.pickle')
        for mentor in data:
            if mentor.name == name and mentor._pwd == pwd:
                return True
    elif(role == "student"):
        data = load_from_pickle('student_data.pickle')
        for student in data:
            if student.name == name and student._pwd == pwd:
                return True
    return False


@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    try:
        if(check_credentials(name, pwd, role)):
            if(role == "mentor"):
                with open('mentor_mentee.pickle', 'rb') as infile:
                    data = pickle.load(infile)

                for mentor_obj, lst_student_obj in data.items():
                    if(mentor_obj.name == name):
                        student_id = [student.id for student in lst_student_obj]
                        student_name = [student.name for student in lst_student_obj]
                        student_details = [student.personal for student in lst_student_obj]

                return render_template("main_mentor.html", ids=student_id, 
                                       names=student_name, details=student_details)
            elif(role == "student"):
                ############ ---------- Work ---------------
                    # Need to create a page called 'main_students.html'
                    # mentee should be able to see only their details, except for the confidential information entered by the mentor
                    # A mentee should be able to request for a meeting with the mentor through this system.
                ############
                pass
            return "Going to your main page ...."
        else:
            return "Invalid Credentials!"
    except KeyError:
        return "Unable to Find Name"
    except Exception as e:
        return f"Error: {e}"

@app.route("/schedule_meeting", methods=['POST'])
def schedule_meeting():
    global notifications
    data = request.get_json()
    mentee_name = data.get('menteeName')

    notification = f'Meeting scheduled for mentee: {mentee_name}'
    notifications.append([mentee_name, notification])

    print(notifications)
    with open('notifications.pickle', 'wb') as outfile:
        pickle.dump(notification, outfile)
    return "Meeting Scheduled"

@app.route("/view_details", methods=["POST", "GET"])
def view_details():
    data = request.get_json()
    mentee_name = data.get("menteeName")

    details = get_details(mentee_name)
    return "Details Are Shown!"

@app.route("/signup_page")
def signup_page():
    return render_template('Signup.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    details = request.form["details"]
    id_info = request.form['id']

    if(role == "mentor"):
        mentor_obj = Mentor(name, pwd, id_info, details)
        write_to_pickle(mentor_obj, 'mentor_data.pickle')
    elif(role == "student"):
        student_obj = Student(name, pwd, id_info, details)
        write_to_pickle(student_obj, 'student_data.pickle')
    return 'SignUp Successful!'

if __name__ == "__main__":
    calculate_mentees()
    app.run(debug = True)