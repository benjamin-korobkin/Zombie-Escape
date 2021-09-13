# KidsCanCode - Game Development with Pygame video series
# Tile-based game
# Video link: https://youtu.be/3UxnelT9aCo
# Music by Eric Matyas
# Weapon icons from Flaticon (attribution required)
# icons.svg from opengameart, qubodup
# landmine by Icons8
# "topdown shooter" art by Kenny.nl
# Weapon pickup by: Guns by Gary <http://fossilrecords.net/>
# licensed under CC-BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>
# "espionage.ogg" by http://opengameart.org/users/haeldb
# Sound effects from freesound.org: KlawyKogut, 

from game import *
from settings import *

# create the game object
g = Game()

while g.running:
    savedata = g.curr_menu.display_menu()
    if g.playing:
        g.load_level(level_name=savedata[0], stats=savedata[1])
        while g.playing:
            g.game_loop()  # Runs the game loop
        if g.game_over:
            g.show_go_screen()
        else:
            g.show_story_screen(LEVELS['ending']['story'])
