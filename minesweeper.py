import random
import time
from collections import deque, namedtuple

Point = namedtuple("Point", ("x", "y"))


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.point = Point(x, y)
        self.adj = 0 # adj to mines number
        self.mine = False
        self.flag = False
        self.visible = False
        self.blow_up = False


    def __repr__(self):
        return f"Square at ({self.x}, {self.y}), mine = {self.mine}, adj = {self.adj}"
    

    # get number of adjacent mines but not mines themselves. Make sure it's in range i.e. .get()
    def get_adjacent_to_mines(self, state):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj != None and adj != self and adj.mine == False:
                    adj.adj += 1


    # get adjacent not-visible squares that aren't mines or flags
    def get_adjacent_recursive_animation(self, state):
        state.to_reveal.appendleft(self)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj != None and adj != self and adj.visible == False and adj not in state.to_reveal:
                    state.to_reveal.appendleft(adj)
                    if adj.adj == 0: # if adj is empty, run again
                        adj.get_adjacent_recursive_animation(state)
    

    def get_adjacent_recursive(self, state):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj != None and adj != self and adj.visible == False:
                    adj.visible = True
                    if adj.adj == 0: # if adj is empty, run again
                        adj.get_adjacent_recursive(state)


    def get_neighbors(self, state):
        neighbors = set()
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                adj = state.squares.get((self.x+dx, self.y+dy), None)
                if adj != None and adj != self:
                    neighbors.add(adj)

        return neighbors


class State:
    def __init__(self):
        
        self.width = 0
        self.height = 0
        self.num_mines = 0

        self.squares = {}

        # board elements
        self.mines = set()
        self.adjacent_to_mines = set()
        self.empty_squares_paths = set()

        self.flags = set()
        self.mines_remaining = 0
        self.selection = None
        self.win = False
        self.lose = False
        self.reset = False
        self.start_clock = False
        self.start_time = time.time()
        self.game_time = 0
        self.score = 0

        self.animate = False
        self.to_reveal = deque() # for animating reveal
        self.revealing_square = None # for animating reveal
        self.origin = None # for animating reveal
        self.frame_count = 0 # for animating reveal
    

    def get_game_time(self):
        return time.time() - self.start_time
    

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

        # create all squares
        self.squares = {(x, y): Square(x, y) for y in range(self.height) for x in range(self.width)}

        # fixed_mines mines for debugging
        if fixed_mines == True:
            self.mines = set(
                self.squares[(mine_coord)] for mine_coord in [
                    (1, 2), (6, 4), (2, 3), (0, 5), (7, 5), (3, 6), (7, 6), (0, 7), (2, 7), (2, 9)
                ]
            )

            for mine in self.mines:
                self.squares[(mine.x, mine.y)].mine = True

        # random mines
        else:
            while len(self.mines) < self.num_mines:
                mine = (self.get_random_coords())
                self.mines.add(self.squares[(mine.x, mine.y)])
                self.squares[(mine.x, mine.y)].mine = True

        # calc adj to mines
        for mine in self.mines:
            mine.get_adjacent_to_mines(state)
        empty_squares = []
        for sq in self.squares.values():
            if sq.mine == False:
                if sq.adj > 0:
                    self.adjacent_to_mines.add(sq)
                else:
                    empty_squares.append(sq)

        self.mines_remaining = self.num_mines - len(self.flags)


    def get_random_coords(self):
        return Point(random.randrange(self.width), random.randrange(self.height))





state = State()
state.create_board(difficulty="easy", fixed_mines=True)
