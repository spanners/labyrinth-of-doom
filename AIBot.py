from LODGame import LODGame
from LODMap import LODMap
import time
class AIBot(object):

    def __init__(self, game, delay=1):
        self.game = game
        self.facing = "N"
        self.y = 2
        self.x = 2
        self.pos = (self.y, self.x)
        while True:
            time.sleep(delay)
            self.look()
            if self.tile_at(self.pos) == game.lodmap.TREASURE:
                self.pickup()
            while self.tile_at(self.next_pos()) == game.lodmap.WALL:
                self.turn_right()
            self.walk()

    def look(self):
        g = self.game
        m = self.game.lodmap
        self.fov = m.parse_map(g.cli_look(),3,3)

    def pickup(self):
        self.game.cli_pickup()

    def move(self, direction):
        self.facing = direction
        self.walk()

    def walk(self):
        facing = self.facing
        if facing == "N":
            self.y -= 1
        elif facing == "S":
            self.y += 1
        elif facing == "E":
            self.x += 1
        elif facing == "W":
            self.x -= 1
        self.game.cli_move(facing)

    def turn_left(self):
        facing = self.facing
        if facing == "N":
            self.facing = "W"
        elif facing == "S":
            self.facing = "E"
        elif facing == "E":
            self.facing = "N"
        elif facing == "W":
            self.facing = "S"

    def turn_right(self):
        facing = self.facing
        if facing == "N":
            self.facing = "E"
        elif facing == "S":
            self.facing = "W"
        elif facing == "E":
            self.facing = "S"
        elif facing == "W":
            self.facing = "N"

    def next_pos(self):
        facing = self.facing
        y = 2
        x = 2
        if facing == "N":
            y -= 1
        elif facing == "S":
            y += 1
        elif facing == "E":
            x += 1
        elif facing == "W":
            x -= 1
        return (y,x)

    def is_tile_at_pos(self, pos):
        return self.fov[pos[0]][pos[1]]

    def is_in_fov(self, tile):
        for row in self.fov:
            for col in row:
                if col == tile:
                    return True
        return False

    def nearest_tile(self, tile):
        j = 0
        i = 0
        for row in self.fov:
            j += 1
            for col in row:
                i += 1
                if col == tile:
                    return (j,i)
        return (-1, -1) # error
