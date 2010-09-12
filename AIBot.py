import time
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
        l = self.game.lodmap
        while True:
            time.sleep(delay)
            self.look()
            if self.tile_in_fov(self.pos) == l.TREASURE:
                #self.pickup()
                pass
            elif self.is_tile_in_fov(game.lodmap.TREASURE):
                nearest = self.nearest_tile_in_fov(game.lodmap.TREASURE)
                print "nearest gold", nearest
                sp = self.shortest_path(nearest)
                print "shortest_path:", sp
                time.sleep(2)
            while self.tile_in_fov(self.next_pos()) == game.lodmap.WALL:
                self.turn_right()
            self.walk()

    def look(self):
        g = self.game
        l = self.game.lodmap
        self.fov = l.parse_map(g.cli_look(),3,3)

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

    def tile_in_fov(self, pos):
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

    def shortest_path(self, target):
        l = self.game.lodmap
        # our (node,weight) queue
        # initialised with the target, and a weight of 0
        queue = [(target,0)]
        # start with first node in the queue
        node = queue[0][0]
        # the weight of the nodes
        weight = 1
        def adj_nodes(node):
            return [(node[0]+1,node[1]), (node[0]-1,node[1]), (node[0],node[1]+1), (node[0],node[1]-1)]
        def elim_nodes(nodes):
            # eliminate all nodes that do not meet criteria:
            i = 0
            while i < len(nodes):
                curr = nodes[i]
                y, x = curr[0], curr[1]
                # 1. outside fov
                if not (y in range(5) and x in range(5)): 
                    del nodes[i]
                    continue
                # 2. impassable
                elif self.fov[y][x] in (l.WALL,l.UNKNOWN,l.OUTSIDE):
                    del nodes[i]
                    continue
                # 3. node already in queue
                elif curr in [n for (n,w) in queue if n == curr]:
                    del nodes[i]
                    continue
                i += 1
            return nodes
        # while we have not pathfound ourselves
        while len([n for (n,w) in queue if n == (2,2)]) < 1:
            # make a list of the adjacent nodes, eliminating invalids
            nodes = elim_nodes(adj_nodes(node))
            # add valid nodes to the queue
            queue[:] = queue + [(n,weight) for n in nodes]
            weight += 1
            weight = weight % len(queue)
            node = queue[weight][0]
        return queue
