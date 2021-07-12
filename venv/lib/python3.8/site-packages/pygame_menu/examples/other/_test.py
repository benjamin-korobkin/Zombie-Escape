"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TEST
Generic tests.

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

import pygame_menu
from pygame_menu.examples import create_example_window

surface = create_example_window('Example - Test', (400, 400))

theme = pygame_menu.themes.THEME_DARK.copy()
theme.title_font_size = 35
theme.widget_selection_effect.zero_margin()
theme.widget_font_size = 25

menu = pygame_menu.Menu(
    column_min_width=400,
    height=400,
    theme=theme,
    title='Color entry',
    onclose=pygame_menu.events.CLOSE,
    width=400
)

# Paste here the example
menu.add.button('rr')
frame = menu.add.frame_h(250, 100, background_color=(200, 0, 0))
btn = menu.add.button('nice1')
menu.add.button('44')
frame2 = menu.add.frame_v(50, 250, background_color=(0, 0, 200))
btn2 = menu.add.button('nice2')
btn3 = menu.add.button('nice3')

frame11 = menu.add.frame_v(50, 90, background_color=(0, 200, 0))

btn11 = menu.add.button('11')
btn12 = menu.add.button('12')

frame11.pack(btn11)
frame11.pack(btn12)

frame.pack(btn)
frame.pack(btn2, pygame_menu.locals.ALIGN_CENTER, vertical_position=pygame_menu.locals.POSITION_CENTER)
frame.pack(frame11, pygame_menu.locals.ALIGN_RIGHT, vertical_position=pygame_menu.locals.POSITION_SOUTH)

frame2.pack(menu.add.button('1'))
frame2.pack(menu.add.button('2'), align=pygame_menu.locals.ALIGN_CENTER)
frame2.pack(menu.add.button('3'), align=pygame_menu.locals.ALIGN_RIGHT)

for w in frame.get_widgets():
    w.get_selection_effect().zero_margin()
for w in frame2.get_widgets():
    w.get_selection_effect().zero_margin()

menu.render()
menu.remove_widget(btn2)
menu.render()

# Don't touch
menu.mainloop(surface)
