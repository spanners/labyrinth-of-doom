import random
import sys
from LODMap import LODMap
class LODGame(object):
    def __init__(self, map_filename):
        self.reset()
        self.lodmap = LODMap(map_filename)
        self.new_game()

    def new_game(self):
        print "STARTING NEW GAME"
        self.start()
        self.rand_start_pos()
        print "Starting At:", self.x, ",", self.y
        print "Goal:", self.lodmap.goal

    def start(self):
        self.ap = 6 - (self.lantern + self.sword + self.armour)

    def reset(self):
        self.name = "Dave"
        self.y = 2
        self.x = 2
        self.lantern = 0
        self.sword = 0
        self.armour = 0
        self.treasure = 0
        self.hp = 3
        self.dead = False
        self.ap = 0

    def check_win(self):
        lodmap = self.lodmap
        if self.treasure >= lodmap.goal and lodmap.map[self.y][self.x] is lodmap.EXIT:
            print "!!!YOU HAVE WON!!!"
            self.reset()
            self.new_game()
        elif self.is_turn_finished():
            self.start()

    def is_turn_finished(self):
        return (self.ap == 0)

    def rand_start_pos(self):
        rand_height = self.get_rand_height()
        rand_width = self.get_rand_width()
        if self.lodmap.map[rand_height][rand_width] != self.lodmap.WALL:
            self.y = rand_height
            self.x = rand_width
        else:
            self.rand_start_pos()

    def get_rand_height(self):
        return random.choice(range(self.lodmap.height))

    def get_rand_width(self):
        return random.choice(range(self.lodmap.width))

    def cli_hello(self, new_name):
        self.name = new_name
        print "HELLO", self.name

    def cli_look(self):
        lodmap = self.lodmap
        distance = 2 + self.lantern
        map = ""
        for i in range(-distance, distance+1):
            line = ""
            for j in range(-distance, distance+1):
                content = "?"
                target_y = self.y + i
                target_x = self.x + j
                if abs(i) + abs(j) > distance + 1:
                    content = "X"
                elif target_y < 0 or target_y >= lodmap.height or target_x < 0 or target_x >= lodmap.width:
                    content = "#"
                else:
                    content = lodmap.int_to_char.get(lodmap.map[target_y][target_x],"G")
                line += content
            map += line + "\n"
        print map[:-1]
        return map[:-1]

    def cli_shout(self, message):
        print message

    def cli_pickup(self):
        lodmap = self.lodmap
        if self.ap > 0:
            s = lodmap.map[self.y][self.x]
            if s == lodmap.EMPTY:
                sys.stderr.write("Nothing to pickup\n")
            elif s == lodmap.HEALTH:
                self.ap = 0
                lodmap.map[self.y][self.x] = lodmap.EMPTY
                print "SUCCESS"
                self.hp += 1
                print "1+ HEALTH"
            elif s == lodmap.LANTERN:
                if self.lantern == 0:
                    self.ap -= 1
                    lodmap.map[self.y][self.x] = lodmap.EMPTY
                    print "SUCCESS"
                    self.lantern = 1
                else:
                    sys.stderr.write("Already have a lantern\n")
            elif s == lodmap.SWORD:
                if self.sword == 0:
                    self.ap -= 1
                    lodmap.map[self.y][self.x] = lodmap.EMPTY
                    print "SUCCESS"
                    self.sword = 1
                else:
                    sys.stderr.write("Already have a sword\n")
            elif s == lodmap.ARMOUR:
                if self.armour == 0:
                    self.ap -= 1
                    lodmap.map[self.y][self.x] = lodmap.EMPTY
                    print "SUCCESS"
                    self.armour = 1
                else:
                    sys.stderr.write("Already have a armour\n")
            else:
                if lodmap.map[self.y][self.x] > 0:
                    self.ap -= 1
                    treasure_picked_up = lodmap.map[self.y][self.x]
                    lodmap.map[self.y][self.x] = lodmap.EMPTY
                    print "SUCCESS"
                    self.treasure += treasure_picked_up
                    print "TREASURE PICKED UP!"
        else:
            sys.stderr.write("No action points left\n")
        if self.ap <= 0:
            self.start()

    def cli_move(self, direction):
        lodmap = self.lodmap
        if self.ap > 0:
            target_y = self.y
            target_x = self.x
            d = direction
            if d == 'N':
                target_y -= 1
            elif d == 'S':
                target_y += 1
            elif d == 'E':
                target_x += 1
            else:
                target_x -= 1

            if target_y >= 0 and target_y < lodmap.height and target_x >= 0 and target_x < lodmap.width:
                if lodmap.map[target_y][target_x] != lodmap.WALL:
                    self.ap -= 1
                    self.y = target_y
                    self.x = target_x
                    print "SUCCESS"
                    self.check_win()
                else:
                    sys.stderr.write("Can not move into a wall\n")
            else:
                sys.stderr.write("Can not move into a wall\n")
        else:
            sys.stderr.write("No action points left\n")

    def cli_attack(self, direction):
        sys.stderr.write("CAN'T ATTACK YET\n")

    def cli_end_turn(self):
        self.ap = 0
        print "END TURN"

