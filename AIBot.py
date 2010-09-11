import time
from heapq import heappush, heappop
import itertools
from LODGame import LODGame
from LODMap import LODMap

class AIBot(object):

    def __init__(self, game, delay=1):
        self.game = game
        self.facing = "N"
        self.y = 2
        self.x = 2
        self.pos = (self.y, self.x)
        self.distance = 2 + game.lantern
        while True:
            time.sleep(delay)
            self.look()
            if self.is_tile_at_pos_in_fov(self.pos) == game.lodmap.TREASURE:
                self.pickup()
            elif self.is_tile_in_fov(game.lodmap.TREASURE):
                nearest = self.nearest_tile_in_fov(game.lodmap.TREASURE)
                print "nearest gold", nearest
                print "pathfind:"
                self.pathfind(nearest)
                time.sleep(2)
            while self.is_tile_at_pos_in_fov(self.next_pos()) == game.lodmap.WALL:
                self.turn_right()
            self.walk()

    def look(self):
        g = self.game
        m = self.game.lodmap
        self.fov = m.parse_map(g.cli_look(),3,3)

    def pickup(self):
        self.game.cli_pickup()
        self.distance = 2 + self.game.lantern

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
        y = x = self.distance
        if facing == "N":
            y -= 1
        elif facing == "S":
            y += 1
        elif facing == "E":
            x += 1
        elif facing == "W":
            x -= 1
        return (y,x)

    def is_tile_at_pos_in_fov(self, pos):
        return self.fov[pos[0]][pos[1]]

    def is_tile_in_fov(self, tile):
        for row in self.fov:
            for col in row:
                if col == tile:
                    return True
        return False

    def tile_positions_in_fov(self, tile):
        tiles = list()
        j = 0
        i = 0
        for row in self.fov:
            for col in row:
                if col == tile:
                    tiles.append((j,i))
                i += 1
            i = 0
            j += 1
        return tiles

    def nearest_tile_in_fov(self, tile):
        tiles = self.tile_positions_in_fov(tile)
        diffs = [(abs(self.distance - tile[0]), abs(self.distance - tile[1])) for tile in tiles]
        i = 0
        minimum = diffs[0]
        for diff in diffs[1:]:
            if sum(diff) < sum(minimum):
                minimum = diff
                i += 1
        return tiles[i]

    def adjacent_cells(self, coord):
        # !! WARNING !! can give you coords outside of lodmap, so test adjacent
        # cells after using this function to obtain them, for example
        # try:
        #   test = self.fov[coord[0]][coord[1]]
        # except IndexError:
        # print "Out of FOV"
        return [(coord[1]+1,coord[0]), (coord[1]-1,coord[0]), (coord[1],coord[0]+1), (coord[1],coord[0]-1)]

    def pathfind(self, coord):
        l = self.game.lodmap              # convenient abbreviation
        queue = []                        # the priority queue list
        add_counter = itertools.count(1)  # unique sequence count
        coord_finder = {}                 # mapping of coords to entries
        INVALID = 0                       # mark an entry as deleted
        pf_iter = 0                       # nonunique sequence count
                                          #   determines which iteration 
                                          #   of the pathfinding alg the coord was added

        def add_coord(pf_iter, coord, add_count=None):
            if add_count is None:
                add_count = next(add_counter)
            entry = [pf_iter, add_count, coord]
            coord_finder[coord] = entry
            heappush(queue, entry)

        def get_lowest_pf_iter():
            while True:
                pf_iter, add_count, coord = heappop(queue)
                del coord_finder[coord]
                if add_count is not INVALID:
                    return coord

        def delete_coord(coord, q=queue):
            entry = coord_finder[coord]
            entry[1] = INVALID # marks entry for deletion by setting count to INVALID
            q[:] = [t for t in q if t[1] != INVALID] # really deletes the coord from q

        def reprioritize(pf_iter, coord):
            entry = coord_finder[coord]
            add_coord(pf_iter, coord, entry[1])
            entry[1] = INVALID

        add_coord(pf_iter, (coord))
        print "queue", queue

        cell = coord

        # loop will start here, for cell in queue
        pf_iter += 1 # counter variable of the current element's counter variable + 1

        # step 1: Create a list of the four adjacent cells
        adj_cells = self.adjacent_cells(cell)
        print "adj_cells", adj_cells
        for c in adj_cells:
            try:
                test = self.fov[c[0]][c[1]] # if this works cell is inside FOV
                add_coord(pf_iter, (c))
            except IndexError: # do not add cells outside of FOV
                continue

        #step 2.1: If the cell is impassable, remove it from the queue 
        print "queue", queue
        for coord in queue:
            c = coord[2]
            if self.fov[c[0]][c[1]] in (l.WALL, l.OUTSIDE, l.UNKNOWN):
                print c, "is impassable", l.int_to_char[self.fov[c[0]][c[1]]]
                delete_coord(c)

        #step 2.2 If there is an element in the main queue with the same coordinate but an equal or higher pf_iter, remove it from the list
        print "queue", queue
        for coord in queue:
            print "coord", coord
            c = coord[2]
            print "c", c
