from LODGame import LODGame
from LODMap import LODMap
import time
class AIBot(object):
    def __init__(self, game, delay=2):
        self.game = game
        self.facing = "N"
        self.x = 0
        self.y = 0
        while True:
            time.sleep(delay)
            self.look()
            self.turn_right()
            self.walk()

    def look(self):
        g = self.game
        m = self.game.lodmap
        self.fov = m.parse_map(g.cli_look(),3,3)

    def walk(self):
        facing = self.facing
        if facing == "N":
            self.y += 1
        elif facing == "S":
            self.y -= 1
        elif facing == "E":
            self.x += 1
        elif facing == "W":
            self.x -= 1
        self.game.cli_move(facing)

    def turn_right(self):
        facing = self.facing
        if facing == "N":
            facing = "E"
        elif facing == "S":
            facing = "W"
        elif facing == "E":
            facing = "S"
        elif facing == "W":
            facing = "N"
