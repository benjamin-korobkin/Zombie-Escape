import pygame as pg
from settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.window_centerx, self.window_centery = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.title_offset = 60
        self.cursor_offsetx = -100
        self.cursor_offsety = -17

    def draw_cursor(self):
        self.game.draw_text('>', self.game.menu_font, 30, WHITE, self.cursor_rect.x, self.cursor_rect.y, align='n')

    def blit_screen(self):
        pg.display.update()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)  # TODO: Use same inheritance technique for sprites
        text_offset = 60
        self.show_continue = False
        self.initial_state = 'new game'
        self.curr_lvl = 'tutorial.tmx'
        self.curr_stats = {
            'accuracy_bonus': 0,
            'fire_rate_bonus': 0,
            'ammo_bonus': 0,
            'dmg_bonus': 0,
            'speed_bonus': 0,
            'bonuses': 0
        }
        try:
            temp_stats = self.curr_stats
            with open('savefile.txt', 'r') as f:
                for stat in self.curr_stats:
                    temp_stats[stat] = int(f.readline())
                lvl = f.readline()
                if not lvl == 'tutorial.tmx':
                    self.show_continue = True
                    self.initial_state = 'continue'
                    self.curr_lvl = lvl
                    for stat in temp_stats:
                        self.curr_stats[stat]
        except:
            print("Trouble reading the save file in menu.py")

        self.state = self.initial_state
        self.continuex, self.continuey = self.window_centerx, self.window_centery - text_offset
        self.newgamex, self.newgamey = self.window_centerx, self.window_centery
        self.optionsx, self.optionsy = self.window_centerx, self.window_centery + text_offset
        self.creditsx, self.creditsy = self.window_centerx, self.window_centery + (text_offset * 2)
        self.quitx, self.quity = self.window_centerx, self.window_centery + (text_offset * 4)
        # TODO: maybe change to center instead of midtop (remove y offset)
        if self.show_continue:
            self.cursor_rect.midtop = (self.continuex + self.cursor_offsetx, self.continuey + self.cursor_offsety)
        else:
            self.cursor_rect.midtop = (self.newgamex + self.cursor_offsetx, self.newgamey + self.cursor_offsety)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('ZOMBIE ESCAPE', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            if self.show_continue:
                self.game.draw_text('Continue', self.game.menu_font, 40, WHITE, self.continuex, self.continuey, 'center')
            self.game.draw_text('New Game', self.game.menu_font, 40, RED, self.newgamex, self.newgamey, 'center')
            self.game.draw_text('Options', self.game.menu_font, 40, WHITE, self.optionsx, self.optionsy, 'center')
            self.game.draw_text('Credits', self.game.menu_font, 40, WHITE, self.creditsx, self.creditsy, 'center')
            self.game.draw_text('Quit', self.game.menu_font, 40, WHITE, self.quitx, self.quity, 'center')
            self.draw_cursor()
            self.blit_screen()
        return [self.curr_lvl, self.curr_stats]


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'continue':
                self.cursor_rect.midtop = (self.newgamex + self.cursor_offsetx, self.newgamey + self.cursor_offsety)
                self.state = 'new game'
            elif self.state == 'new game':
                self.cursor_rect.midtop = (self.optionsx + self.cursor_offsetx, self.optionsy + self.cursor_offsety)
                self.state = 'options'
            elif self.state == 'options':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offsetx, self.creditsy + self.cursor_offsety)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (self.quitx + self.cursor_offsetx, self.quity + self.cursor_offsety)
                self.state = 'quit'
            elif self.state == 'quit':
                if self.show_continue:
                    self.cursor_rect.midtop = (
                    self.continuex + self.cursor_offsetx, self.continuey + self.cursor_offsety)
                    self.state = 'continue'
                else:
                    self.cursor_rect.midtop = (self.newgamex + self.cursor_offsetx, self.newgamey + self.cursor_offsety)
                    self.state = 'new game'
            self.game.DOWN_KEY = False

        if self.game.UP_KEY:
            if self.state == 'continue':
                self.cursor_rect.midtop = (self.quitx + self.cursor_offsetx, self.quity + self.cursor_offsety)
                self.state = 'quit'
            elif self.state == 'new game':
                if self.show_continue:
                    self.cursor_rect.midtop = (self.continuex + self.cursor_offsetx, self.continuey + self.cursor_offsety)
                    self.state = 'continue'
                else:
                    self.cursor_rect.midtop = (self.quitx + self.cursor_offsetx, self.quity + self.cursor_offsety)
                    self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offsetx, self.creditsy + self.cursor_offsety)
                self.state = 'credits'
            elif self.state == 'options':
                self.cursor_rect.midtop = (self.newgamex + self.cursor_offsetx, self.newgamey + self.cursor_offsety)
                self.state = 'new game'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (self.optionsx + self.cursor_offsetx, self.optionsy + self.cursor_offsety)
                self.state = 'options'
            self.game.UP_KEY = False
        self.game.reset_keys()

    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'continue':
                self.game.playing = True
            if self.state == 'new game':
                self.curr_lvl = 'tutorial.tmx'
                self.game.playing = True
            elif self.state == 'options':
                self.game.curr_menu = self.game.options_menu
            elif self.state == 'credits':
                self.game.curr_menu = self.game.credits_menu
            elif self.state == 'quit':
                self.game.quit()
            self.game.START_KEY = False
            self.run_display = False
        self.move_cursor()

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        text_offset = 60
        self.initial_state = 'volume'
        self.state = self.initial_state
        self.volumex, self.volumey = self.window_centerx, self.window_centery
        self.controlsx, self.controlsy = self.window_centerx, self.window_centery + text_offset
        self.backx, self.backy = self.window_centerx, self.window_centery + (text_offset * 3)
        # TODO: maybe change to center instead of midtop (remove y offset)
        self.cursor_rect.midtop = (self.volumex + self.cursor_offsetx, self.volumey + self.cursor_offsety)
        self.prev_menu = MainMenu

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('OPTIONS', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            self.game.draw_text('Volume', self.game.menu_font, 40, WHITE, self.volumex, self.volumey, 'center')
            self.game.draw_text('Controls', self.game.menu_font, 40, WHITE, self.controlsx, self.controlsy, 'center')
            self.game.draw_text('Back', self.game.menu_font, 40, WHITE, self.backx, self.backy, 'center')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'volume':
                self.cursor_rect.midtop = (self.controlsx + self.cursor_offsetx, self.controlsy + self.cursor_offsety)
                self.state = 'controls'
            elif self.state == 'controls':
                self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)
                self.state = 'back'
            elif self.state == 'back':
                self.cursor_rect.midtop = (self.volumex + self.cursor_offsetx, self.volumey + self.cursor_offsety)
                self.state = 'volume'
            self.game.DOWN_KEY = False
        elif self.game.UP_KEY:
            if self.state == 'volume':
                self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)
                self.state = 'back'
            elif self.state == 'controls':
                self.cursor_rect.midtop = (self.volumex + self.cursor_offsetx, self.volumey + self.cursor_offsety)
                self.state = 'volume'
            elif self.state == 'back':
                self.cursor_rect.midtop = (self.controlsx + self.cursor_offsetx, self.controlsy + self.cursor_offsety)
                self.state = 'controls'
            self.game.UP_KEY = False

    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'volume':
                self.game.curr_menu = self.game.volume_menu
            elif self.state == 'controls':
                self.game.curr_menu = self.game.controls_menu
            elif self.state == 'back':
                self.game.curr_menu = self.game.main_menu
            self.game.START_KEY = False
            self.run_display = False
        elif self.game.BACK_KEY or (self.game.START_KEY and self.state == 'back'):
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        self.move_cursor()

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        text_offset = 60
        self.initial_state = 'credits'
        self.state = self.initial_state
        self.tutorialsx, self.tutorialsy = self.window_centerx, self.window_centery - text_offset * 3
        self.artx, self.arty = self.window_centerx, self.window_centery - text_offset * 2
        self.other_artx, self.other_arty = self.window_centerx, self.window_centery - text_offset
        self.audiox, self.audioy = self.window_centerx, self.window_centery
        self.fontx, self.fonty = self.window_centerx, self.window_centery + text_offset
        self.see_morex, self.see_morey = self.window_centerx, self.window_centery + text_offset * 2
        self.backx, self.backy = self.window_centerx, self.window_centery + text_offset * 5

        # TODO: maybe change to center instead of midtop (remove y offset)
        self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)
        self.prev_menu = MainMenu

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('CREDITS', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            self.game.draw_text('PYGAME TUTORIALS -- KidsCanCode and Christian Duenas', self.game.menu_font, 40, WHITE,
                                self.tutorialsx, self.tutorialsy, 'center')
            self.game.draw_text('MAIN ART -- Kenney', self.game.menu_font, 40, WHITE, self.artx, self.arty, 'center')
            self.game.draw_text('Other Art -- Flaticon, qubodup, Icons8'
                                , self.game.menu_font, 40, WHITE, self.other_artx, self.other_arty, 'center')
            self.game.draw_text('Audio -- Eric Matyas and ', self.game.menu_font, 40, WHITE, self.audiox,
                                self.audioy, 'center')
            self.game.draw_text('Font -- Michael Gene Adkins', self.game.menu_font, 40, WHITE, self.fontx, self.fonty, 'center')
            self.game.draw_text('See more in main.py', self.game.menu_font, 40, WHITE, self.see_morex, self.see_morey, 'center')
            self.game.draw_text('Back', self.game.menu_font, 40, WHITE, self.backx, self.backy, 'center')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        self.game.reset_keys()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            self.game.reset_keys()
        self.move_cursor()

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        text_offset = 60
        self.initial_state = 'soundfx'
        self.state = self.initial_state
        self.soundfxx, self.soundfxy = self.window_centerx, self.window_centery
        self.musicx, self.musicy = self.window_centerx, self.window_centery + text_offset
        self.backx, self.backy = self.window_centerx, self.window_centery + text_offset * 5
        self.cursor_rect.midtop = (self.soundfxx + self.cursor_offsetx, self.soundfxy + self.cursor_offsety)
        self.sample_snd = self.game.weapon_sounds['pistol'][0]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('VOLUME', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            self.game.draw_text('Change volumes using left-right arrow keys', self.game.menu_font, 35, WHITE,
                                self.window_centerx, self.title_offset + 85, 'n')
            self.game.draw_text('SoundFX - ' + str(int(self.game.soundfx_lvl * 10)), self.game.menu_font, 40, WHITE, self.soundfxx, self.soundfxy, 'center')
            self.game.draw_text('Music - ' + str(int(self.game.music_lvl * 10)), self.game.menu_font, 40, WHITE, self.musicx, self.musicy, 'center')
            self.game.draw_text('Back', self.game.menu_font, 40, WHITE, self.backx, self.backy, 'center')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'soundfx':
                self.cursor_rect.midtop = (self.musicx + self.cursor_offsetx, self.musicy + self.cursor_offsety)
                self.state = 'music'
            elif self.state == 'music':
                self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)
                self.state = 'back'
            elif self.state == 'back':
                self.cursor_rect.midtop = (self.soundfxx + self.cursor_offsetx, self.soundfxy + self.cursor_offsety)
                self.state = 'soundfx'
        elif self.game.UP_KEY:
            if self.state == 'soundfx':
                self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)
                self.state = 'back'
            elif self.state == 'music':
                self.cursor_rect.midtop = (self.soundfxx + self.cursor_offsetx, self.soundfxy + self.cursor_offsety)
                self.state = 'soundfx'
            elif self.state == 'back':
                self.cursor_rect.midtop = (self.musicx + self.cursor_offsetx, self.musicy + self.cursor_offsety)
                self.state = 'music'

    def check_input(self):
        self.move_cursor()
        if self.game.LEFT_KEY:
            if self.state == 'soundfx' and self.game.soundfx_lvl >= 0.1:
                self.game.soundfx_lvl -= .1
                self.sample_snd.set_volume(self.game.soundfx_lvl)
                self.sample_snd.play()
            elif self.state == 'music' and self.game.music_lvl >= 0.1:
                self.game.music_lvl -= .1
                pg.mixer.music.set_volume(self.game.music_lvl)
        elif self.game.RIGHT_KEY:
            if self.state == 'soundfx' and self.game.soundfx_lvl < 1:
                self.game.soundfx_lvl += .1
                self.sample_snd.set_volume(self.game.soundfx_lvl)
                self.sample_snd.play()
            elif self.state == 'music' and self.game.music_lvl < 1:
                self.game.music_lvl += .1
                pg.mixer.music.set_volume(self.game.music_lvl)
        elif self.game.BACK_KEY or (self.game.START_KEY and self.state == 'back'):
            self.game.curr_menu = self.game.options_menu
            self.run_display = False
        self.game.reset_keys()

class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        text_offset = 60
        self.initial_state = 'resume'
        self.state = self.initial_state
        self.resumex, self.resumey = self.window_centerx, self.window_centery - text_offset
        self.soundfxx, self.soundfxy = self.window_centerx, self.window_centery
        self.musicx, self.musicy = self.window_centerx, self.window_centery + text_offset
        self.toggle_fsx, self.toggle_fsy = self.window_centerx, self.window_centery + text_offset * 2
        self.save_quitx, self.save_quity = self.window_centerx, self.window_centery + text_offset * 5
        self.cursor_rect.midtop = (self.resumex + self.cursor_offsetx, self.resumey + self.cursor_offsety)
        self.sample_snd = self.game.weapon_sounds['pistol'][0]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.dt = self.game.clock.tick(FPS) / 1000  # THIS MIGHT BE IT!!!
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('PAUSED', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            self.game.draw_text('Resume', self.game.menu_font, 40, RED, self.resumex, self.resumey, 'center')
            self.game.draw_text('SoundFX - ' + str(int(self.game.soundfx_lvl * 10)), self.game.menu_font, 40, WHITE, self.soundfxx, self.soundfxy, 'center')
            self.game.draw_text('Music - ' + str(int(self.game.music_lvl * 10)), self.game.menu_font, 40, WHITE, self.musicx, self.musicy, 'center')
            self.game.draw_text('Toggle Fullscreen', self.game.menu_font, 40, WHITE, self.toggle_fsx, self.toggle_fsy,
                                'center')
            self.game.draw_text('Save and Quit', self.game.menu_font, 40, WHITE, self.save_quitx, self.save_quity, 'center')

            self.draw_cursor()
            self.blit_screen()  # Not the problem

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'resume':
                self.cursor_rect.midtop = (self.soundfxx + self.cursor_offsetx, self.soundfxy + self.cursor_offsety)
                self.state = 'soundfx'
            elif self.state == 'soundfx':
                self.cursor_rect.midtop = (self.musicx + self.cursor_offsetx, self.musicy + self.cursor_offsety)
                self.state = 'music'
            elif self.state == 'music':
                self.cursor_rect.midtop = (self.toggle_fsx + self.cursor_offsetx - 40, self.toggle_fsy + self.cursor_offsety)
                self.state = 'toggle_fs'
            elif self.state == 'toggle_fs':
                self.cursor_rect.midtop = (self.save_quitx + self.cursor_offsetx, self.save_quity + self.cursor_offsety)
                self.state = 'save_quit'
            elif self.state == 'save_quit':
                self.cursor_rect.midtop = (self.resumex + self.cursor_offsetx, self.resumey + self.cursor_offsety)
                self.state = 'resume'
        elif self.game.UP_KEY:
            if self.state == 'resume':
                self.cursor_rect.midtop = (self.save_quitx + self.cursor_offsetx, self.save_quity + self.cursor_offsety)
                self.state = 'save_quit'
            elif self.state == 'soundfx':
                self.cursor_rect.midtop = (self.resumex + self.cursor_offsetx, self.resumey + self.cursor_offsety)
                self.state = 'resume'
            elif self.state == 'music':
                self.cursor_rect.midtop = (self.soundfxx + self.cursor_offsetx, self.soundfxy + self.cursor_offsety)
                self.state = 'soundfx'
            elif self.state == 'toggle_fs':
                self.cursor_rect.midtop = (self.musicx + self.cursor_offsetx, self.musicy + self.cursor_offsety)
                self.state = 'music'
            elif self.state == 'save_quit':
                self.cursor_rect.midtop = (self.toggle_fsx + self.cursor_offsetx - 40, self.toggle_fsy + self.cursor_offsety)
                self.state = 'toggle_fs'

    def check_input(self):
        self.move_cursor()
        if self.game.LEFT_KEY:
            if self.state == 'soundfx' and self.game.soundfx_lvl >= 0.1:
                self.game.soundfx_lvl -= .1
                self.sample_snd.set_volume(self.game.soundfx_lvl)
                self.sample_snd.play()
            elif self.state == 'music' and self.game.music_lvl >= 0.1:
                self.game.music_lvl -= .1
                pg.mixer.music.set_volume(self.game.music_lvl)
        elif self.game.RIGHT_KEY:
            if self.state == 'soundfx' and self.game.soundfx_lvl < 1:
                self.game.soundfx_lvl += .1
                self.sample_snd.set_volume(self.game.soundfx_lvl)
                self.sample_snd.play()
            elif self.state == 'music' and self.game.music_lvl < 1:
                self.game.music_lvl += .1
                pg.mixer.music.set_volume(self.game.music_lvl)
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.paused = False
        elif self.game.START_KEY:
            if self.state == 'resume':
                self.run_display = False
                self.game.paused = False
            elif self.state == 'toggle_fs':
                self.game.toggle_fullscreen()
            elif self.state == 'save_quit':
                self.game.quit()
        self.game.reset_keys()


class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        text_offset = 60
        self.initial_state = 'controls'
        self.state = self.initial_state
        self.movex, self.movey = self.window_centerx, self.window_centery - text_offset * 3
        self.shootx, self.shooty = self.window_centerx, self.window_centery - text_offset * 2
        self.change_weaponx, self.change_weapony = self.window_centerx, self.window_centery - text_offset
        self.place_minex, self.place_miney = self.window_centerx, self.window_centery
        self.pausex, self.pausey = self.window_centerx, self.window_centery + text_offset
        self.toggle_fsx, self.toggle_fsy = self.window_centerx, self.window_centery + text_offset * 2
        self.backx, self.backy = self.window_centerx, self.window_centery + text_offset * 5
        self.cursor_rect.midtop = (self.backx + self.cursor_offsetx, self.backy + self.cursor_offsety)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.menu_events()
            self.check_input()
            self.game.screen.fill(BLACK)
            self.game.draw_text('CONTROLS', self.game.menu_font, 60, WHITE, self.window_centerx,
                                self.title_offset, 'n')
            self.game.draw_text('MOVE  ---  Arrow keys', self.game.menu_font, 40, WHITE, self.movex, self.movey, 'center')
            self.game.draw_text('SHOOT  ---  SPACEBAR', self.game.menu_font, 40, WHITE, self.shootx, self.shooty, 'center')
            self.game.draw_text('Change weapon  ---  C', self.game.menu_font, 40, WHITE, self.change_weaponx,
                                self.change_weapony, 'center')
            self.game.draw_text('Place landmine  ---  X', self.game.menu_font, 40, WHITE, self.place_minex,
                                self.place_miney, 'center')
            self.game.draw_text('Pause --- P', self.game.menu_font, 40, WHITE, self.pausex, self.pausey, 'center')
            self.game.draw_text('Toggle Fullscreen --- F4 - in-game only', self.game.menu_font, 40, WHITE, self.toggle_fsx,
                                self.toggle_fsy, 'center')
            self.game.draw_text('Back', self.game.menu_font, 40, WHITE, self.backx, self.backy, 'center')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        self.game.reset_keys()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.options_menu
            self.run_display = False
        self.move_cursor()

