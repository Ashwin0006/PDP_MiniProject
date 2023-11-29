from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/studentlogin", methods=['POST', 'GET'])
def studentlogin():
    return "Done!"

if __name__ == "__main__":
    app.run(debug = True)