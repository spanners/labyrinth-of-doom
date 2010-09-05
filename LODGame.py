import random
import sys
from LODMap import LODMap
class LODGame(object):
    def __init__(self):
        self.reset()
        self.lodmap = LODMap()
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
        if self.treasure >= self.lodmap.goal and self.lodmap.map[self.y][self.x] is self.lodmap.EXIT:
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
        distance = 2 + self.lantern
        for i in range(-distance, distance+1):
            line = ""
            for j in range(-distance, distance+1):
                content = "?"
                target_y = self.y + i
                target_x = self.x + j
                if abs(i) + abs(j) > distance + 1:
                    content = "X"
                elif target_y < 0 or target_y >= self.lodmap.height or target_x < 0 or target_x >= self.lodmap.width:
                    content = "#"
                else:
                    content = self.lodmap.int_to_char.get(self.lodmap.map[target_y][target_x],'G')
                line += content
            print line

    def cli_shout(self, message):
        print message

    def cli_pickup(self):
        if self.ap > 0:
            s = self.lodmap.map[self.y][self.x]
            if s == self.lodmap.EMPTY:
                sys.stderr.write("Nothing to pickup")
            elif s == self.lodmap.HEALTH:
                self.ap = 0
                self.lodmap.map[self.y][self.x] = self.lodmap.EMPTY
                print "SUCCESS"
                self.hp += 1
                print "1+ HEALTH"
            elif s == self.lodmap.LANTERN:
                if self.lantern == 0:
                    self.ap -= 1
                    self.lodmap.map[self.y][self.x] = self.lodmap.EMPTY
                    print "SUCCESS"
                    self.lantern = 1
                else:
                    sys.stderr.write("Already have a lantern")
            elif s == self.lodmap.SWORD:
                if self.sword == 0:
                    self.ap -= 1
                    self.lodmap.map[self.y][self.x] = self.lodmap.EMPTY
                    print "SUCCESS"
                    self.sword = 1
                else:
                    sys.stderr.write("Already have a sword")
            elif s == self.lodmap.ARMOUR:
                if self.armour == 0:
                    self.ap -= 1
                    self.lodmap.map[self.y][self.x] = self.lodmap.EMPTY
                    print "SUCCESS"
                    self.armour = 1
                else:
                    sys.stderr.write("Already have a armour")
            else:
                if self.lodmap.map[self.y][self.x] > 0:
                    self.ap -= 1
                    treasure_picked_up = self.lodmap.map[self.y][self.x]
                    self.lodmap.map[self.y][self.x] = self.lodmap.EMPTY
                    print "SUCCESS"
                    self.treasure += treasure_picked_up
                    print "TREASURE PICKED UP!"
        else:
            sys.stderr.write("No action points left")
        if self.ap <= 0:
            self.start()

    def cli_move(self, direction):
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

            if target_y >= 0 and target_y < self.lodmap.height and target_x >= 0 and target_x < self.lodmap.width:
                if self.lodmap.map[target_y][target_x] != self.lodmap.WALL:
                    self.ap -= 1
                    self.y = target_y
                    self.x = target_x
                    print "SUCCESS"
                    self.check_win()
                else:
                    sys.stderr.write("Can not move into a wall")
            else:
                sys.stderr.write("Can not move into a wall")
        else:
            sys.stderr.write("No action points left")

    def cli_attack(self, direction):
        sys.stderr.write("CAN'T ATTACK YET")

    def cli_end_turn(self):
        self.ap = 0
        print "END TURN"

