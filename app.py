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

    # GET - create board and send
    if fl.request.method == "GET":
        # Create board calling minesweeper
        mstate = ms.State()
        mstate.create_board(difficulty="easy", fixed_mines=True)
        
        # Send to client as a dict
        data = mstate.setup_packet()

        return fl.render_template("minesweeper.html", data = data)

    # POST - receive requests and update board
    elif fl.request.method == "POST":
        print(f"request: {fl.request.form}")

        # Square index from client
        square_idx = fl.request.form.get("square")

        # Only return data if game not over
        if square_idx and not mstate.game_over:
            mstate.update_server(square_idx)
            
            # Return to mines or visible squares to client
            response = mstate.update_packet()

            print(f"returning: {response}")
            
            return response

        # flask requires a return value; 204 status will keep browser on current page
        return ("", 204)
    

# template for button once things are established
# <!-- <button onclick="checkSquare()" class="square" name="b" id="{{ }}"></button> -->