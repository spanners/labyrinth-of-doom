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
        self.pickup()
      elif self.is_tile_in_fov(l.TREASURE):
        nearest = self.nearest_tile_in_fov(l.TREASURE)
        print "nearest gold", nearest
        try:
          sp = self.shortest_path((2, 2), nearest)
          print "shortest_path:", sp
        except Exception as e:
          print "path broken around", e
        time.sleep(2)
      while self.tile_in_fov(self.next_pos()) == l.WALL:
        self.turn_right()
      self.walk()

  def look(self):
    g = self.game
    l = self.game.lodmap
    self.fov = l.parse_map(g.cli_look(), 3, 3)

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
          tiles.append((j, i))
        i += 1
      i = 0
      j += 1
    return tiles

  def nearest_tile_in_fov(self, tile):
    tiles = self.tile_positions_in_fov(tile)
    diffs = [(abs(self.distance - tile[0]), 
      abs(self.distance - tile[1])) for tile in tiles]
    i = 0
    minimum = diffs[0]
    for diff in diffs[1:]:
      if sum(diff) < sum(minimum):
        minimum = diff
        i += 1
    return tiles[i]

  def shortest_path(self, start, end):
    """Finds the shortest path from start to end

    Args:
      start: (y, x) coordinate of the start
      end: (y, x) coordinate of the end

    Returns:
      queue: A list of the form [((y, x), weight), ...] with the weights of
      each node in the path from start to end.
    """

    l = self.game.lodmap
    # our (node,weight) queue
    queue = [(end, 0)]

    def adj_nodes(node):
      """Find the coordinates of all 4 adjacent nodes.
      
      Args:
        node: The (y,x) node

      Returns:
        A list of nodes N,E,S and W of arg node.
      """
      return [(node[0] + 1, node[1]), (node[0] - 1, node[1]),
          (node[0], node[1] + 1), (node[0], node[1] - 1)]

    def elim_nodes(nodes):
        """Eliminate all nodes that do not meet criteria.

        Args:
          nodes: A list of (y, x) coordinates that may contain impassable
            objects, outside FOV or already in queue.

        Returns:
          nodes: A list of valid (y, x) coordinates.
        """
        i = 0
        while i < len(nodes):
          curr = nodes[i]
          y, x = curr[0], curr[1]
          # 1. outside fov
          if not (y in range(5) and x in range(5)): 
            del nodes[i]
            continue
          # 2. impassable
          elif self.fov[y][x] in (l.WALL, l.UNKNOWN, l.OUTSIDE):
            del nodes[i]
            continue
          # 3. node already in queue
          elif curr in [n for (n, w) in queue if n == curr]:
            del nodes[i]
            continue
          i += 1
        return nodes

    node = queue[0][0] # current node we're exploring
    len_before = len(queue)
    len_after = 0
    weight = 1 # the weight of the nodes
    visited_nodes = list()
    while start not in [n for (n, w) in queue]:
      if len_before == len_after and node in visited_nodes:
        raise Exception(queue[-1][0])
      nodes = elim_nodes(adj_nodes(node))
      visited_nodes.append(node)
      len_before = len(queue)
      queue[:] = queue + [(n, weight) for n in nodes]
      len_after = len(queue)
      weight = (weight + 1) % len(queue)
      node = queue[weight][0]
    return queue
