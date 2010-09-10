from LODGame import LODGame
from AIBot import AIBot
import sys
class PlayGame(object):
    def __init__(self, map_filename):
        self.game = LODGame(map_filename)
        ai_bot = AIBot(self.game, 0.5)
        self.play()

    def play(self):
        while 1:
            try:
                self.game.cli_look()
                self.player_command(raw_input())
            except (KeyboardInterrupt,EOFError):
                break

    def player_command(self, command):
        tmp = command.split(" ", 2)
        com = tmp[0]
        arg = False
        if len(tmp) == 2:
            arg = tmp[1]

        if com == "HELLO":
            if len(tmp) == 2:
                self.game.cli_hello(arg)
        elif com == "PICKUP":
            self.game.cli_pickup()
        elif com == "MOVE":
            if len(tmp) != 2:
                print "Needs direction"
                return
            direction = arg.upper()
            if direction in ("N","E","S","W"):
                self.game.cli_move(direction)
            else:
                print "Invalid direction"
        elif com == "ATTACK":
            if len(tmp) != 2:
                print "Needs direction"
                return
            if direction in ("N","E","S","W"):
                self.game.cli_attack(direction)
            else:
                print "Invalid direction"
        elif com == "ENDTURN":
            self.game.cli_end_turn()
        elif com == "SHOUT":
            self.game.cli_shout(arg)
        else:
            print "Invalid command"

if __name__ == "__main__":
    PlayGame(sys.argv[1])
