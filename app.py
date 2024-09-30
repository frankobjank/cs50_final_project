import flask

# link to access app for debug http://127.0.0.1:5000

# Configure application
app = flask.Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    return flask.render_template("index.html")


@app.route("/minesweeper")
def minesweeper():

    return flask.render_template("minesweeper.html")