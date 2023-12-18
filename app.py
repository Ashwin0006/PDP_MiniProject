from flask import Flask, render_template, request
import json
import pickle


app = Flask(__name__)
notifications = []
# with open('notifications.pickle', 'rb') as infile:
#     notifications = pickle.load(infile)
#     print(notifications)

def load_from_json(path):
    try:
        with open(path, 'r') as outfile:
            data = json.load(outfile)
    except:
        data = {"admin" : ("admin", "mentor")}
        write_to_json(path, data)
    return data

def write_to_json(path, data):
    with open(path, 'w') as infile:
        json.dump(data, infile)

def calculate_mentees():
    data = load_from_json("data.json")
    mentors = []
    mentees = []
    for key in data:
        if(data[key][1] == 'mentor'):
            mentors.append(key)
        else:
            mentees.append(key)

    mentor_mentee_pair = []
    for mentor in mentors:
        label = [mentor]
        mentor_mentee_pair.append(label)
    
    i = 0
    j = 0
    while(j < len(mentees)):
        mentor_mentee_pair[i].append(mentees[j])
        j += 1
        i += 1
        i = i % len(mentors)
    final_data = {}
    for i in mentor_mentee_pair:
        mentor = i[0]
        mentees_list = i[1:]
        final_data[mentor] = mentees_list
    print(final_data)
    with open('mentor_mentee.pickle', 'wb') as outfile:
        pickle.dump(final_data, outfile)
        

@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    data = load_from_json("data.json")
    try:
        if(data[name][0] == pwd and data[name][1] == role):
            if(role == "mentor"):
                results = []
                with open('mentor_mentee.pickle', 'rb') as infile:
                    data = pickle.load(infile)
                for mentor in data:
                    if(mentor == name):
                        results = data[mentor]
                return render_template("main_mentor.html", mentees=results)
            elif(role == "student"):
                ############ ---------- Work ---------------
                    # Need to create a page called 'main_students.html'
                    # mentee should be able to see only their details, except for the confidential information entered by the mentor
                    # A mentee should be able to request for a meeting with the mentor through this system.
                ############
                pass
            return "Going to your main page ...."
        else:
            return "Invalid Password or Role"
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

    with open('notifications.pickle', 'wb') as outfile:
        pickle.dump(notification, outfile)
    return "Meeting Scheduled"

@app.route("/signup_page")
def signup_page():
    return render_template('Signup.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    proof = request.form["proof"]
    if(proof == "yes"):
        data = load_from_json("data.json")
        data[name] = (pwd, role)
        write_to_json("data.json", data)
        calculate_mentees()
        return 'SignUp Successful!'
    else:
        return("Invalid Proof!")
if __name__ == "__main__":
    calculate_mentees()
    app.run(debug = True)