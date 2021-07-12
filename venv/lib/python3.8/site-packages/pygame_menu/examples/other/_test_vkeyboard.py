"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TEST
Test virtual keyboard, https://github.com/Faylixe/pygame-vkeyboard.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import sys

sys.path.insert(0, '../../')
sys.path.insert(0, '../../../')

import pygame
import pygame_menu
from pygame_vkeyboard import *
from pygame_menu.examples import create_example_window

FPS = 30

surface = create_example_window('Example - Test', (500, 500))
clock = pygame.time.Clock()

menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)

user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)


def consumer(text: str) -> None:
    """
    Text from virtual keyboard to input.
    """
    user_name.set_value(text)


# Initializes and activates the keyboard
layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
keyboard = VKeyboard(surface, consumer, layout)

while True:

    # Tick
    clock.tick(FPS)

    surface.fill((0, 0, 0))

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if keyboard.is_enabled():
                keyboard.disable()
            else:
                keyboard.enable()

    # Main menu
    menu.update(events)
    keyboard.update(events)

    menu.draw(surface)
    if keyboard.is_enabled():
        user_name.translate(0, -50)
        keyboard.draw(surface, force=True)
    else:
        user_name.translate(0, 0)

    # Flip surface
    pygame.display.flip()
