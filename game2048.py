import pew
import random


class Game2048:
    COLOR_BLACK = 0
    COLOR_GREEN = 1
    COLOR_RED = 2
    COLOR_YELLOW = 3

    BLINK_RARE = lambda x: x % 2 != 0
    BLINK_OFTEN = lambda x: x % 5 != 0
    BLINK_NONE = lambda x: True

    ITEMS = {
        2: (BLINK_RARE, COLOR_RED),
        4: (BLINK_OFTEN, COLOR_RED),
        8: (BLINK_NONE, COLOR_RED),
        16: (BLINK_RARE, COLOR_YELLOW),
        32: (BLINK_OFTEN, COLOR_YELLOW),
        64: (BLINK_NONE, COLOR_YELLOW),
        128: (BLINK_RARE, COLOR_GREEN),
        256: (BLINK_OFTEN, COLOR_GREEN),
        512: (BLINK_NONE, COLOR_GREEN),
    }

    state = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def add_random_items(self):
        """
        Add new items to the free cells
        """
        for i in range(2):
            x, y = -1, -1
            while self.state[x][y] != 0:
                x, y = random.randint(0, 7), random.randint(0, 7)
            self.state[x][y] = random.choice([2, 2, 2, 4])

    def get_color(self, item, blinking):
        """
        Depending on blinking return either original color or black
        :param item: int
        :param blinking: int, blinking state
        :return: int
        """
        if item == 0:
            return item
        return self.ITEMS[item][1] if self.ITEMS[item][0](blinking) else 0

    def get_board(self, blinking):
        """
        Consider blinking before board rendering
        :param blinking:
        :return:
        """
        board = []
        for m in range(len(self.state)):
            board.append([])
            for n in range(len(self.state[m])):
                board[m].append(self.get_color(self.state[m][n], blinking))
        return board

    def get_params(self, keys):
        params_by_key = {
            pew.K_RIGHT: {
                "step_x": 1,
                "step_y": 0,
                "horizontal": (6, -1, -1),
                "vertical": (0, 8, 1)
            },
            pew.K_LEFT: {
                "step_x": -1,
                "step_y": 0,
                "horizontal": (1, 8, 1),
                "vertical": (0, 8, 1)
            },
            pew.K_UP: {
                "step_x": 0,
                "step_y": -1,
                "horizontal": (0, 8, 1),
                "vertical": (1, 8, 1)
            },
            pew.K_DOWN: {
                "step_x": 0,
                "step_y": 1,
                "horizontal": (0, 8, 1),
                "vertical": (6, -1, -1)
            },
        }
        return params_by_key.get(keys)

    def move(self, keys):
        """
        Move items to needed direction.
        :param keys:
        :return:
        """
        params = self.get_params(keys)
        if not params:
            return

        step_x, step_y, horizontal, vertical = params.values()
        movements = set()  # list of already concatenated items.
        game_over = True
        for y in range(*vertical):
            for x in range(*horizontal):
                if self.state[y][x] != 0:
                    value = self.state[y][x]
                    curr_y, curr_x = y, x
                    next_y, next_x = y + step_y, x + step_x
                    while all([
                        0 <= next_x <= 7,
                        0 <= next_y <= 7,
                    ]):
                        if self.state[next_y][next_x] not in [0, self.state[curr_y][curr_x]]:
                            break
                        elif self.state[next_y][next_x] == self.state[curr_y][curr_x] and (
                                next_y, next_x) not in movements:
                            game_over = False
                            self.state[next_y][next_x] += value
                            self.state[curr_y][curr_x] = 0
                            if self.state[next_y][next_x] not in self.ITEMS:
                                pew.Pix.from_text("YOU WON!")
                            movements.add((next_y, next_x))
                            break
                        elif self.state[next_y][next_x] == 0:
                            game_over = False
                            self.state[next_y][next_x] += value
                            self.state[curr_y][curr_x] = 0
                            movements.add((next_y, next_x))
                        if (curr_y, curr_x) in movements:
                            movements.remove((curr_y, curr_x))
                        curr_x += step_x
                        curr_y += step_y
                        next_x += step_x
                        next_y += step_y
                    else:
                        if self.state[curr_y][curr_x] == value:
                            movements.add((curr_y, curr_x))

        if not game_over:
            pew.Pix.from_text("GAME OVER!")


pew.init()
screen = pew.Pix()
blinking = 0
add_in = 0
game = Game2048()

while True:
    if add_in == 0:
        game.add_random_items()
        add_in = None
    elif add_in:
        add_in -= 1

    blinking = 0 if blinking == 9 else blinking + 1
    board = pew.Pix.from_iter(game.get_board(blinking))
    keys = pew.keys()
    if keys != 0 and not add_in:
        add_in = 10  # add new items after some delay
        game.move(keys)
    screen.blit(board)
    pew.show(screen)
    pew.tick(1 / 128)
