import flask as fl
import minesweeper_game
from flask_session import Session
import sqlite3
from time import time, strftime, localtime

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
    # Set user_id to 1 for debug
    fl.session["user_id"] = "1"

    return fl.render_template("index.html")


@app.route("/minesweeper", methods=["GET", "POST"])
def minesweeper():
    
    # POST - receive requests and update board
    if fl.request.method == "POST":
        
        print(f"request: {fl.request.form}")

        # Redirect to initial `get` request on reset
        if fl.request.form.get("reset"):
            fl.redirect("/minesweeper")

        # Retrieve minesweeper state from session
        ms = fl.session.get("ms")

        # Square index from client
        square_idx = fl.request.form.get("square")

        # Only return data if game not over
        if square_idx and not (ms.win or ms.lose):
            ms.update_server(square_idx)
            
            # Connect to database on gameover; should only happen once
            if ms.game_over:
                
                # Validate score received from client to prevent cheating
                server_score = int(ms.score)
                client_score = int(fl.request.form.get("score"))

                # Test if margin of error is less than 20%
                if abs(server_score - client_score) < (0.2 * server_score):
                    server_score = client_score

                print(f"SERVER TIME {server_score}")
                print(f"CLIENT TIME {client_score}")

                # Update database
                with sqlite3.connect("database.db") as conn:
                    conn.execute(
                        """
                        INSERT INTO ms_stats (mode, score, win, date, user_id)
                        VALUES (?, ?, ?, ?, ?)
                        """, (
                            ms.difficulty,         # mode
                            client_score,          # score
                            ms.win,                # win
                            int(time()),           # date
                            fl.session["user_id"]  # user_id
                        )
                    )
                    
            # Return mines, visible squares to client
            response = ms.update_packet()
            print(f"returning: {response}")
            
            # Banner for win; might have to add to response somehow
            # if ms.win:
                # fl.flash("Congratulations! You win!")
            
            return response

        print(f"returning nothing; 204")
        # flask requires a return value; 204 status will keep browser on current page
        return ("", 204)

    # GET - create board and send
    elif fl.request.method == "GET":
        # Set user_id to 1 for debug
        fl.session["user_id"] = "1"

        # Get difficulty from client; defaults to easy
        difficulty = fl.request.args.get("difficulty", "easy")

        # Create new minesweeper State object; add to flask session to access later
        fl.session["ms"] = minesweeper_game.State()
        fl.session["ms"].create_board(difficulty=difficulty)  # , fixed_mines=True)

        # Send to client as dict
        return fl.render_template("minesweeper.html", data=fl.session["ms"].setup_packet())


@app.route("/minesweeper/stats")
def minesweeper_stats():
    db_responses = {}  # {"easy": [], "medium": [], "hard": []}
    
    # Query database and retrieve the stats
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        modes = ["easy", "medium", "hard"]

        # To do in one transaction, could sort into mode as 
        for mode in modes:
            db_responses[mode] = conn.execute(
                "SELECT score, win FROM ms_stats WHERE user_id = ? AND mode = ? AND score != 0", ("1", mode)
            )

    ### To format date::
    # for mode, response in db_responses.items():
        # for r in response:
            # r["date"] = strftime("%Y-%m-%d %H:%M:%S", localtime(r["date"]))
            # print(f"{mode}: {r}")

    # Calculate win rate and average time for win
    data = {"easy": {}, "medium": {}, "hard": {}}  # {"easy": {win_rate: 0, average_score: 0}...}

    modes = ["easy", "medium", "hard"]

    for mode in modes:
        games_won = 0.0
        total_scores = 0.0
        for row in db_responses[mode]:
            if row["win"]:
                games_won += row["win"]
                total_scores += row["score"]
        
        total_games = float(len(db_responses))
        
        data[mode]["win_rate"] = round(games_won/total_games, 2)
        data[mode]["average_score"] = round(total_scores/total_games, 2)

    return fl.render_template("minesweeper_stats.html", data=data)


# Add user manually; not live on site yet; no password
def register(user_id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO users (username, date) VALUES (?, ?)", (user_id, int(time())))

# For returning SQL as dict
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}