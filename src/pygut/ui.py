from typing import Sequence

import pygame
from pygut.base import UIElement, Screen
import pygut

class Menu(Screen):
    '''A screen comprised of entirely UIElements.
       Can display things to the user, or have buttons that the user can click to interact with.
       Pass overlay to **kwargs to turn the Menu into an overlayed screen instead of replacing the current one.
       Note: overlay param currently does not have implementation. That will be added in a future update.'''
    def __init__(self, bg: pygame.Surface | pygame.Color, elements: Sequence[UIElement], **kwargs):
        super().__init__(bg, elements, **kwargs)

class Button(UIElement):
    def __init__(self, x: float, y: float, render: pygame.Surface | str, action, **kwargs):
        super().__init__(x, y, render, **kwargs)
        
        def check():
            if self.rect.collidepoint(pygame.mouse.get_pos()): action()
        self.add_action(pygut.M1, pygut.K_PRESSED, check)