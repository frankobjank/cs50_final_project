import random
import time
from collections import namedtuple


Point = namedtuple("Point", ("x", "y"))


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adj = 0 # adj to mines number
        self.mine = False
        self.visible = False


    def __repr__(self):
        return f"Square at ({self.x}, {self.y}), mine = {self.mine}, adj = {self.adj}"


    # get number of adjacent mines but not mines themselves. Make sure it's in range i.e. .get()
    def get_adjacent_to_mines(self, state):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj is not None and adj != self and not adj.mine:
                    adj.adj += 1
    

    def get_adjacent_recursive(self, state):

        # Double for-loop to get all adjacent squares
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj is not None and adj != self and not adj.visible:
                    adj.visible = True
                    state.visible.add(adj)
                    
                    # If adj is empty, run again
                    if adj.adj == 0: 
                        adj.get_adjacent_recursive(state)


    def get_neighbors(self, state):
        neighbors = set()
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj is not None and adj != self:
                    neighbors.add(adj)

        return neighbors


class State:
    def __init__(self):
        
        # Board Elements
        self.width = 0
        self.height = 0
        self.num_mines = 0

        # Board Collections
        self.squares = {}
        self.mines = set()
        self.adjacent_to_mines = set()
        self.visible = set()

        # Win/Lose
        self.win = False
        self.lose = False
        self.reset = False
        self.blow_up = None

        # Timing
        self.start_clock = False
        self.start_time = time.time()
        self.game_time = 0
        self.score = 0
    

    def get_game_time(self):
        return time.time() - self.start_time
    

    def coords_to_index(self, coords: tuple) -> int:
        # validate
        if len(coords) != 2:
            print("Tuple must have 2 items.")
            return None

        if coords[0] > self.width - 1 or coords[1] > self.height - 1:
            print("Coords out of bounds.")
            return None

        # y * self.width + x
        return coords[1] * self.width + coords[0]


    def index_to_coords(self, i: int) -> tuple:
        # validate
        if i > self.height * self.width:
            print("Index out of bounds.")
            return None

        # Can use modulo or divmod
        # x = i % self.width, y = i // self.width

        dm = divmod(i, self.width)
        return (dm[1], dm[0])


    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.width, self.height, self.num_mines = 10, 10, 10
        elif difficulty == "medium":
            self.width, self.height, self.num_mines = 16, 16, 40
        elif difficulty == "hard":
            self.width, self.height, self.num_mines =  30, 16, 99


    def create_board(self, difficulty, fixed_mines=False):
        # set dimensions based on difficulty
        self.set_difficulty(difficulty)

        # create all squares - dict
        self.squares = {(x, y): Square(x, y) for y in range(self.height) for x in range(self.width)}

        # Fixed_mines mines for debugging
        if fixed_mines:
            self.mines = set(
                self.squares[(mine_coord)] for mine_coord in [
                    (1, 2), (6, 4), (2, 3), (0, 5), (7, 5),
                    (3, 6), (7, 6), (0, 7), (2, 7), (2, 9)])

            for mine in self.mines:
                self.squares[(mine.x, mine.y)].mine = True

        # Assign random mines; not debug
        else:
            while len(self.mines) < self.num_mines:
                mine = (self.get_random_coords())
                self.mines.add(self.squares[(mine.x, mine.y)])
                self.squares[(mine.x, mine.y)].mine = True

        # Calc adj to mines
        for mine in self.mines:
            mine.get_adjacent_to_mines(state=self)
        empty_squares = []
        for sq in self.squares.values():
            if not sq.mine:
                if sq.adj > 0:
                    self.adjacent_to_mines.add(sq)
                else:
                    empty_squares.append(sq)


    def get_random_coords(self):
        return Point(random.randrange(self.width), random.randrange(self.height))


    def setup_packet(self):
        # Only need dimensions; keep mines and adj info hidden on server side
        return {"width": self.width, "height": self.height, "num_mines": self.num_mines}


    def update_server(self, selection_index: str):
        
        # Convert index to int and access squares dict
        square = self.squares[self.index_to_coords(int(selection_index))]
        
        # Hit mine; game over
        if square.mine:
            self.lose = True
            self.blow_up = square

            # Game over; freeze time
            self.score = self.get_game_time()

        # Hit a number
        elif square.adj > 0: 
            square.visible = True
            self.visible.add(square)

        # Hit empty space; check to reveal additional spaces
        else:
            square.visible = True
            self.visible.add(square)
            square.get_adjacent_recursive(self)
        
        if self.check_for_win():
            self.win = True


    def update_packet(self):
        # Reveal adj, vis, mines as needed
        packet = {"adj": [], "visible": [], "mines": [], "win": False}
        
        if self.lose:
            packet["mines"] = [self.coords_to_index((m.x, m.y)) for m in self.mines]

        # Append index of visible square and adj value corresponding with that square
        for s in self.squares.values():
            if s.visible:
                packet["adj"].append(s.adj)
                packet["visible"].append(self.coords_to_index((s.x, s.y)))
        
        assert len(packet["adj"]) == len(packet["visible"]), "len of adj and visible should match"
            
        return packet


    def check_for_win(self):
        # Check if all non-mine squares are visible
        return len(self.visible) == (self.width * self.height) - len(self.mines)


# state = State()
# state.create_board(difficulty="easy", fixed_mines=True)
