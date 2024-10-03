import flask as fl
import minesweeper as ms
from flask_session import Session

# link to access app for debug http://127.0.0.1:5000

# Configure application
app = fl.Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    return fl.render_template("index.html")


@app.route("/minesweeper", methods=["GET", "POST"])
def minesweeper():

    if fl.request.method == "POST":

        print(fl.request.form)
        
        # flask requires a return value; 204 status will keep browser on current page
        return ("", 204)

    else:
        return fl.render_template("minesweeper.html")