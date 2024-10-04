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

    # Create board calling minesweeper
    mstate = ms.State()
    mstate.create_board(difficulty="easy", fixed_mines=True)
    
    if fl.request.method == "POST":
        print(fl.request.form)
        square_idx = fl.request.form.get("square")

        if square_idx:
            mstate.check_move(square_idx)

            # Return to client indices of newly visible squares
            
        # flask requires a return value; 204 status will keep browser on current page
        return ("", 204)

    else:

        # Send to client as a dict
        data = mstate.build_packet()

        return fl.render_template("minesweeper.html", data = data)
    

# template for button once things are established
# <!-- <button onclick="checkSquare()" class="square" name="b" id="{{ }}"></button> -->