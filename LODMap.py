class LODMap(object):
    def __init__(self):
        self.TREASURE = 1
        self.EMPTY = 0
        self.HEALTH = -1
        self.LANTERN = -2
        self.SWORD = -3
        self.ARMOUR = -4
        self.EXIT = -5
        self.WALL = -6
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
                self.WALL:"#"
                }
