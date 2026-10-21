import sys
from typing import Sequence
import pygame
from pygame.sprite import DirtySprite, LayeredDirty
from pygame.font import Font

class _element(DirtySprite):
    '''Root of the entity hierarchy. Defines a basic entity that is drawn to the screen every frame.
       Optional collider param to specify interactions with other entities. Without a collider the object has no physics.'''
    def __init__(self, x: float, y: float, image: pygame.Surface, collider: 'Collider | None' = None):
        super().__init__()
        
        self.pos = pygame.math.Vector2(x, y)
        
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        
        if not collider is None:
            self.collider = collider
    
    def update(self, *args, **kwargs):
        '''Called once per frame by the group self sprite is in. dt is passed into kwargs, use when overriding for time-based updates.
           If the sprite is changed, set dirty=1 to redraw.'''
           
    def move(self, x: float, y: float):
        self.pos.x += x
        self.pos.y += y

        if self.collider:
            self.collider.pos.x += x
            self.collider.pos.y += y

class GameElement(_element):
    '''Object with a collider that is drawn to the screen. Mainly a class to be distinct from UIElement class for UI elements.'''
    def __init__(self, x: float, y: float, image: pygame.Surface, collider: 'Collider'):
        super().__init__(x, y, image, collider)
        
class UIElement(_element):
    '''Object to be drawn to the screen above all of the GameObjects. Image to be rendered may be a string passed into render parameter.
       If render is a string, also pass the arguments font and font_color into kwargs for use.'''
    def __init__(self, x: float, y: float, render: pygame.Surface | str, **kwargs):
        if type(render) is str:
            try:
                font: Font = kwargs['font']
                image = font.render(render, False, kwargs['font_color'])
            except:
                print('Something went wrong. Check that you\'re passing both font and font_color into kwargs.')
                sys.exit()
        else: image = render
        
        assert type(image) is pygame.Surface
        
        super().__init__(x, y, image)

class Collider:
    '''Base hitbox object to store the position of an object. Subclasses can add functionality such as a physics engine.
       x,y is the center of the object.'''
    def __init__(self, x: float, y: float):
        self.pos = pygame.math.Vector2(x, y)
    
    def collides(self, other: 'Collider') -> bool:
        self_vect = self._truncated_line(other)
        other_vect = other._truncated_line(self)
        if self.pos.x < other.pos.x:
            return self.pos.x + self_vect.x >= other.pos.x + other_vect.x
        else:
            return self.pos.x + self_vect.x <= other.pos.x + other_vect.x
    
    def _truncated_line(self, other: 'Collider') -> pygame.math.Vector2: ...

class Screen(pygame.Surface):
    '''An object to be drawn to the screen. Has a collection of GameElements and UIElements that are drawn to the screen.'''
    def __init__(self, bg: pygame.color.Color | pygame.Surface, elements: Sequence[_element] | None = None, **kwargs):
        self.elements = LayeredDirty()
        self.game_elements = []
        self.ui_elements = []
        self.bg = bg
        
        size: tuple[int, int] = pygame.display.get_window_size()
        
        if kwargs['overlay'] == True:
            assert type(kwargs['size']) is tuple[int, int]
            size = kwargs['size']
            
        super().__init__(size, flags=kwargs['flags'])
        
        if not elements is None:
            for e in elements:
                args = {}
                if type(e) is UIElement: 
                    args['layer'] = 1
                    self.ui_elements.append(e)
                else: self.game_elements.append(e)
                self.elements.add(e, args)
    
    def update(self, dt: float):
        self.elements.update(dt=dt)

class Timer:
    '''Class that defines a timer that ticks down a set number of seconds. Updates an optional dependent when the timer is done.'''
    def __init__(self, time: float, start_max: bool, dependent: 'Dependent | None' = None):
        self.dependent = dependent
        
        self.default_time = time
        
        if start_max:
            self.time = time
        else:
            self.time = 0
        
    def countdown(self, dt: float) -> bool:
        self.time -= dt
        if self.time > 0:
            return False
        
        if not self.dependent == None:
            self.dependent.action()
        return True

    def reset(self, time: float | None = None):
        if time is None:
            self.time = self.default_time
        else:
            self.time = time

class Dependent:
    '''Object that is notified to perform an action when its timer finishes counting down.'''
    def __init__(self, action, time: int, timer_list: list[Timer]):
        self.action = action
        depends_on = Timer(time, True)
        timer_list.append(depends_on)