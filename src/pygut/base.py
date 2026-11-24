import sys
from types import FunctionType
from typing import Collection, Union
import pygame
from pygame.sprite import Sprite, LayeredUpdates
from pygame.font import Font
import pygut
from pygut._internal import add_to_dict, remove_from_dict, check_actions
import pygut.collider

_STATE = 0
_ACTION = 1

Point = Union[pygame.Vector2, tuple[int,int], list[int,int]]

class Element(Sprite):
    '''Root of the entity hierarchy. Defines a basic entity that is drawn to the screen every frame.
       Optional collider param to specify interactions with other entities. Without a collider the object has no physics.'''
    def __init__(self, pos: Point, image: pygame.Surface, collider: pygut.collider.Collider | None = None):
        super().__init__()
        
        if isinstance(pos, (tuple, list)):
            x = pos[0]
            y = pos[1]
        else:
            x = pos.x
            y = pos.y
        
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(pos)
        
        if not collider is None:
            self.collider = collider
            
        self.actions = {}
                    
    def add_action(self, key: int, state: int, action):
        add_to_dict(self.actions, key, [state, action])
    
    def update(self, *args, **kwargs):
        '''Called once per frame by the group self sprite is in. dt is passed into kwargs, use when overriding for time-based updates.'''
    
    def move(self, dist):
        self.rect.move_ip(dist)
        self.pos += dist

class GameElement(Element):
    '''Object with a collider that is drawn to the screen. Mainly a class to be distinct from UIElement class for UI elements.'''
    def __init__(self, pos: Point, image: pygame.Surface, collider: pygut.collider.Collider):
        super().__init__(pos, image, collider)
    
    def move(self, dist):
        super().move(dist)
        self.collider.move(dist)
    
class UIElement(Element):
    '''Object to be drawn to the screen above all of the GameObjects. Image to be rendered may be a string passed into render parameter.
       If render is a string, also pass the arguments font and font_color into kwargs for use.'''
    def __init__(self, pos: Point, render: pygame.Surface | str, **kwargs):
        if isinstance(render, str):
            try:
                font: Font = kwargs['font']
                image = font.render(render, False, kwargs['font_color'])
            except KeyError:
                print('Something went wrong. Check that you\'re passing both font and font_color into kwargs.')
                pygame.quit()
                sys.exit()
        else: image = render
        
        super().__init__(pos, image)

class Screen(pygame.Surface):
    '''An object to be drawn to the screen. Has a collection of GameElements and UIElements that are drawn to the screen.'''
    def __init__(self, bg: pygame.Color | tuple | pygame.Surface, elements: Collection[Element] | None = None, **kwargs):
        self.elements = LayeredUpdates()
        self.game_elements = []
        self.ui_elements = []
        
        size: tuple[int, int] = pygut.app.win.size
        try:
            if kwargs['overlay'] == True:
                size = kwargs['size']
                super().__init__(size, flags=kwargs['flags'])
        except KeyError:
            super().__init__(size)
        
        if isinstance(bg, (pygame.Color, tuple)):
            self.fill(bg)
        else:
            self.blit(bg, (0,0))
        
        self.k_down_actions = {}
        self.k_up_actions = {}
        self.k_held_actions = {}
        
        if not elements is None:
            for e in elements:
                self.add(e)
    
    def update(self, **kwargs):
        check_actions(self)
        
        self.elements.update(**kwargs)
    
    def add_action(self, key, state, action):
        match state:
            case pygut.K_PRESSED:
                add_to_dict(self.k_down_actions, key, action)
            case pygut.K_RELEASED:
                add_to_dict(self.k_up_actions, key, action)
            case pygut.K_HELD:
                add_to_dict(self.k_held_actions, key, action)
    
    def remove_action(self, key, state, action):
        match state:
            case pygut.K_PRESSED:
                remove_from_dict(self.k_down_actions, key, action)
            case pygut.K_RELEASED:
                remove_from_dict(self.k_down_actions, key, action)
            case pygut.K_HELD:
                remove_from_dict(self.k_held_actions, key, action)
    
    def add(self, e: Element):
        if isinstance(e, UIElement):
            self.ui_elements.append(e)
            self.elements.add(e, layer=1)
        else: 
            self.game_elements.append(e)
            self.elements.add(e)
            
        for button in e.actions.keys():
            for action in e.actions[button]:
                self.add_action(button, action[_STATE], action[_ACTION])
    
    def add_all(self, elements: Collection[Element]):
        for e in elements:
            self.add(e)
    
    def remove(self, e: Element):
        self.elements.remove(e)
        try:
            if isinstance(e, GameElement):
                self.game_elements.remove(e)
            else:
                self.ui_elements.remove(e)
        except ValueError: pass
        
    def remove_all(self, elements: Collection[Element]):
        for e in elements:
            self.remove(e)

class Timer:
    '''Class that defines a timer that ticks down a set number of seconds. Calls an optional method when the timer is done.'''
    def __init__(self, time: float, start_max: bool, on_complete: FunctionType | None = None, on_reset: FunctionType | None = None):
        self.on_complete = on_complete
        self.on_reset = on_reset
        
        self.default_time = time
        
        if start_max:
            self.time = time
        else:
            self.time = 0
        
    def countdown(self, dt: float) -> bool:
        if self.time == 0: return
        
        self.time -= dt
        if self.time > 0:
            return False
        
        self.time = 0
        if self.on_complete is not None:
            self.on_complete()
        return True

    def reset(self, time: float | None = None):
        if time is None:
            self.time = self.default_time
        else:
            self.time = time
        
        if self.on_reset is not None:
            self.on_reset()