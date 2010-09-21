#!/usr/bin/env python2.4
import itertools
import time
import operator

def izip_longest(*args, **kwds):
    # izip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
    fillvalue = kwds.get('fillvalue')
    def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
        yield counter()         # yields the fillvalue, or raises IndexError
    fillers = itertools.repeat(fillvalue)
    iters = [itertools.chain(it, sentinel(), fillers) for it in args]
    try:
        for tup in itertools.izip(*iters):
            yield tup
    except IndexError:
        pass

def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  """Groups iterable into n sized yields, filling gaps with fillvalue.

  Copied from http://docs.python.org/library/itertools.html#recipes

  Returns:
    A generator of the groups.
  """
  args = [iter(iterable)] * n
  return izip_longest(fillvalue=fillvalue, *args)

class BrokenPathException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class AIBot(object):
  def __init__(self, game, delay=1):
    self.game = game
    self.facing = "N"
    self.y = 2
    self.x = 2
    self.pos = (self.y, self.x)
    self.distance = 2 + game.lantern
    self.span = (self.distance * 2) + 1

    try:
      self.main_loop(delay)
    except (KeyboardInterrupt, EOFError):
      pass

  def look(self):
    g = self.game
    l = self.game.lodmap
    self.fov = l.parse_map(g.cli_look())

  def pickup(self):
    self.game.cli_pickup()
    self.distance = 2 + self.game.lantern
    self.span = (self.distance * 2) + 1

  def move(self, direction):
    self.facing = direction
    self.walk()

  def walk(self, do_look=True):
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
    if do_look:
      self.look()

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
    tiles = []
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
  
  def nearest_tiles(self, tile):
    "nearest_tiles(TREASURE) --> [(2, 0), (0, 2), (0, 3)]"
    """Finds the positions of the nearest tiles in the bot's field of vision.

    Args:
      tile: The type of tile you want to find the coordinates of e.g.
      self.game.lodmap.TREASURE.

    Returns:
      A list of the tiles positions sorted in ascending
        order by manhattan distance from the bot e.g. [(2, 0), (0, 2), (0, 3)].
    """

    def sort_tiles_by_dist(tiles_dists):
      "sort_tiles_by_dist({(0, 2):2, (2, 0):1, (0, 3):3}) --> [(2, 0), (0, 2), (0, 3)]"
      return [k for k,v in sorted(tiles_dists.iteritems(), key=operator.itemgetter(1))]

    tiles_pos = self.tile_positions_in_fov(tile)
    manhattan_dists = [(abs(self.distance - pos[0]) +
      abs(self.distance - pos[1])) for pos in tiles_pos]
    return sort_tiles_by_dist(dict(zip(tiles_pos, manhattan_dists)))

  def a_star(self, start, goal):
    "a_star((2, 2), (4, 1)) --> [(3, 2), (3, 1), (4, 1)]"
    """Finds shortest path between start and goal.

    Adapted from http://en.wikipedia.org/wiki/A*_search_algorithm

    Args:
      start: (y, x) coordinate of the start of the path you want to find.
        Usually the bot's current position, self.pos.
      goal: (y, x) coordinate of where you want to get to.

    Returns:
      Shortest path between start and goal, not including the start, including
        the goal.

    Raises:
      BrokenPathException(f_score): If the path can not be found.
    """

    def heuristic_estimate_of_distance(start, goal):
      return 0

    def node_with_lowest_f_score(f_score, openset):
      lowest_scoring_node = openset[0]
      i = 0
      for node in openset:
        if f_score[node] < f_score[lowest_scoring_node]:
          lowest_scoring_node = node
        i += 0
      return (lowest_scoring_node, i)

    def neighbour_nodes(node):
      "neighbour_nodes((2, 2)) --> [(1, 2), (2, 3), (3, 2), (2, 1)]"
      """Finds the valid neighbouring nodes to node.

      Args:
        node: The (y, x) of the node you want to find the neighbouring nodes
          of.

      Returns:
        A list of the valid (inside the field of vision, and passable) nodes
          that are neighbours of node.
      """

      nodes = [(node[0] + 1, node[1]),  # N
          (node[0], node[1] + 1),       # E
          (node[0] - 1, node[1]),       # S
          (node[0], node[1] - 1)]       # W
      i = 0
      # Remove invalid nodes:
      while i < len(nodes):
        curr = nodes[i]
        y, x = curr[0], curr[1]
        # 1. Outside FOV
        if not (y in range(self.span) and x in range(self.span)):
          del nodes[i]
          continue
        # 2. Impassable
        elif self.tile_in_fov(curr) in (l.WALL, l.UNKNOWN, l.OUTSIDE):
          del nodes[i]
          continue
        i += 1
      return nodes

    def reconstruct_path(came_from, current_node):
      if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        return (p + current_node)
      else:
        return current_node

    l = self.game.lodmap

    closedset = [] # The set of nodes already evaluated.
    openset = [start] # The set of tentative nodes to be evaluated.
    came_from = {} # The map of navigated nodes.
    g_score = {start: 0} # Distance from start along optimal path.
    h_score = {start: heuristic_estimate_of_distance(start, goal)}
    f_score = {start: h_score[start]} # Estimated total distance from start to goal through y.
    while len(openset) != 0:
      x, x_index = node_with_lowest_f_score(f_score, openset)
      if x == goal:
        return [pair for pair in grouper(2, reconstruct_path(came_from,
          came_from[goal]))][1:] + [goal]
      del openset[x_index]
      closedset.append(x)
      for y in neighbour_nodes(x):
        if y in closedset:
          continue
        tentative_g_score = g_score[x] + heuristic_estimate_of_distance(x, y)

        if not y in openset:
          openset.append(y)
          tentative_is_better = True
        elif tentative_g_score < g_score[y]:
          tentative_is_better = True
        else:
          tentative_is_better = False
        if tentative_is_better:
          came_from[y] = x
          g_score[y] = tentative_g_score
          h_score[y] = heuristic_estimate_of_distance(y, goal)
          f_score[y] = g_score[y] + h_score[y]
    raise BrokenPathException(f_score)

  def walk_path(self, pos, path):
    def direction_of_adjacent_node(node, adj_node):
      if adj_node[0] == node[0]:
        if adj_node[1] < node[1]:
          return "W"
        else:
          return "E"
      else:
        if adj_node[0] < node[0]:
          return "N"
        else:
          return "S"
    directions = []
    for node in path:
      directions.append(direction_of_adjacent_node(pos, node))
      pos = node
    for direction in directions:
      self.move(direction)
      
  def main_loop(self, delay):
    l = self.game.lodmap
    self.look() # initialise the field of vision self.fov
    while True:
      time.sleep(delay)
      # pickup gold we spawned on top of
      if self.tile_in_fov(self.pos) == l.TREASURE:
        self.pickup()
      # pathfind to gold
      elif self.is_tile_in_fov(l.TREASURE):
        nearest_tiles = self.nearest_tiles(l.TREASURE)
        for target in nearest_tiles:
          # try to get to the nearest target
          try:
            path = self.a_star((2, 2), target)
            # if we can pathfind to it, pick it up
            self.walk_path((2, 2), path)
            self.pickup()
            break
          except BrokenPathException:
            # otherwise, try the next nearest target
            continue 
      # turn away from walls
      while self.tile_in_fov(self.next_pos()) == l.WALL:
        self.turn_right()
      self.walk()
