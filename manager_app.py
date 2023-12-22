from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def manager_home():
    return "Hello Manager"


if(__name__ == "__main__"):
    app.run(debug=True)