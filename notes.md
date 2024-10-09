# Notes

removed `flask_session.Session(app)` from app.py since not dealing with usernames/passwords yet. Might need for multiplayer compatibility.

implement a basic sql alchemy db just to get it working - can update schema later

## Stats

* compare score with personal score for size
* compare score with global score for size
* win/loss rate?

## Tables

### Users

* id
* username
* password_hash

### Rounds

* id
* size_board
* user_id
* time (score)
