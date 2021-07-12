# KidsCanCode - Game Development with Pygame video series
# Tile-based game
# Video link: https://youtu.be/3UxnelT9aCo
# Credit to Kenney for Game Art
# Credit to Eric Matyas for Music
# Weapon icons from Flaticon (attribution required)
# (Credit creator of icons.svg, opengameart) qubodup
# landmine by Icons8
# "topdown shooter" art by Kenny.nl
# Weapon pickup by: Guns by Gary <http://fossilrecords.net/> licensed under CC-BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>
# "espionage.ogg" by http://opengameart.org/users/haeldb

from game import *

# create the game object
g = Game()
while g.running:
    # g.show_menu_screen("PRESS ANY KEY TO BEGIN")
    lvl = g.curr_menu.display_menu()
    if g.playing:
        g.load_level(level_name=lvl)
        while g.playing:
            g.game_loop()  # Runs the game loop
            g.show_go_screen()
