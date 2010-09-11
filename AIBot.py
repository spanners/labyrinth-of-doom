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
        return [(coord[1]+1,coord[0]), (coord[1]-1,coord[0]), (coord[1],coord[0]+1), (coord[1],coord[0]-1)]

    def pathfind(self, coord):
        pq = []                         # the priority queue list
        counter = itertools.count(1)    # unique sequence count
        task_finder = {}                # mapping of tasks to entries
        INVALID = 0                     # mark an entry as deleted

        def add_task(priority, task, count=None):
            if count is None:
                count = next(counter)
            entry = [priority, count, task]
            task_finder[task] = entry
            heappush(pq, entry)

        def get_top_priority():
            while True:
                priority, count, task = heappop(pq)
                del task_finder[task]
                if count is not INVALID:
                    return task

        def delete_task(task, pri_queue=pq):
            entry = task_finder[task]
            entry[1] = INVALID # marks entry for deletion by setting count to INVALID
            pri_queue[:] = [t for t in pri_queue if t[1] != INVALID] # really deletes the task from pri_queue

        def reprioritize(priority, task):
            entry = task_finder[task]
            add_task(priority, task, entry[1])
            entry[1] = INVALID

        l = self.game.lodmap

        pri = 0
        add_task(pri, (coord))
        print "pq", pq

        cell = coord
        pri += 1

        adj_cells = self.adjacent_cells(cell)
        print "adj_cells", adj_cells
        for c in adj_cells:
            try:
                if self.fov[c[0]][c[1]] in range(-8, 2):
                    add_task(pri, (c))
            except IndexError:
                continue

        #step 2.1: If the cell is impassable, remove it from the list
        print "pq", pq
        for task in pq:
            c = task[2]
            if self.fov[c[0]][c[1]] in (l.WALL, l.OUTSIDE, l.UNKNOWN):
                print c, "is impassable", l.int_to_char[self.fov[c[0]][c[1]]]
                delete_task(c)

        #step 2.2 If there is an element in the main list with the same coordinate and an equal or higher priority (lower number), remove it from the list
        print "pq", pq
        for task in pq:
            print "task", task
            c = task[2]
            print "c", c
