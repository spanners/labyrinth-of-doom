class LODMap(object):
  def __init__(self, map_filename):
    self.TREASURE = 1
    self.EMPTY = 0
    self.HEALTH = -1
    self.LANTERN = -2
    self.SWORD = -3
    self.ARMOUR = -4
    self.EXIT = -5
    self.WALL = -6
    self.OUTSIDE = -7
    self.UNKNOWN = -8
    self.height = 5
    self.width = 5
    self.goal = 2
    self.map = [
        [self.WALL,    self.WALL,     self.ARMOUR,  self.WALL,     self.WALL    ],
        [self.WALL,    self.EXIT,     self.EMPTY,   self.TREASURE, self.TREASURE],
        [self.LANTERN, self.TREASURE, self.EMPTY,   self.HEALTH,   self.LANTERN ],
        [self.WALL,    self.SWORD,    self.EMPTY,   self.ARMOUR,   self.TREASURE],
        [self.WALL,    self.WALL,     self.SWORD,   self.WALL,     self.WALL    ]
        ]
    self.int_to_char = {
        self.EMPTY:".",
        self.HEALTH:"H",
        self.LANTERN:"L",
        self.SWORD:"S",
        self.ARMOUR:"A",
        self.EXIT:"E",
        self.WALL:"#",
        self.OUTSIDE:"X",
        self.UNKNOWN:"?",
        self.TREASURE:"G"
        }
    self.char_to_int = dict((v,k) for k, v in self.int_to_char.iteritems())
    self.char_to_int["G"] = 1
    self.parse(map_filename)

  def parse(self, map_filename):
    map_file = open(map_filename)
    map_string = ''.join(map_file.readlines())
    tmp = map_string.split("\n", 2)
    self.name = tmp[0].split(" ", 2)[1]
    self.goal = tmp[1].split(" ", 2)[1]
    self.height = len(tmp[2].split("\n")) - 1
    self.width = tmp[2].index("\n")
    self.map = self.parse_map(tmp[2], self.height, self.width)

  def parse_map(self, map_string, height, width):
    map = list()
    map.append(list())
    i = 0
    for c in map_string:
        if c == '\n':
            map.append(list())
            i += 1
        else:
            map[i].append(self.char_to_int[c])
    return map
