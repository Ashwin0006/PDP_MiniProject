import pickle
import json

# First Run the file for initial saves of data

if __name__ == "__main__":
    with open('mentor_data.pickle', 'wb') as outfile:
        data = []
        pickle.dump(data, outfile)
    
    with open('student_data.pickle', 'wb') as outfile:
        data = []
        pickle.dump(data, outfile)

    with open('notifications.json', 'w') as file:
        json.dump([], file)

        