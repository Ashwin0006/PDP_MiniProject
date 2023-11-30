from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/studentlogin", methods=['POST', 'GET'])
def studentlogin():
    return "Done!"

@app.route("/signup_page")
def signup_page():
    return render_template('Signup.html')

if __name__ == "__main__":
    app.run(debug = True)