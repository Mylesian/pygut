import pygame
from typing import Union
import pygut.const

def add_to_dict(dict: dict, key, val):
    if key in dict.keys():
        dict[key].append(val)
    else:
        dict[key] = [val]
        
def remove_from_dict(dict: dict, key, val):
    if key in dict.keys():
        dict[key].remove(val)
        
        if len(dict[key]) == 0:
            del dict[key]
            
Point = Union[pygame.Vector2, tuple[int,int], list[int,int]]
def convert_point(pt: Point):
    if isinstance(pt, pygame.Vector2):
        pt = (pt.x, pt.y)
    
    return pt

def check_actions(self):
    just_pressed = pygame.key.get_just_pressed()
    just_released = pygame.key.get_just_released()
    pressed = pygame.key.get_pressed()
    mouse_just_pressed = pygame.mouse.get_just_pressed()
    mouse_just_released = pygame.mouse.get_just_released()
    mouse_pressed = pygame.mouse.get_pressed()
    
    for key in self.k_down_actions.keys():
        if key not in pygut.const.MOUSE_KEYS:
            if just_pressed[key]:
                for action in self.k_down_actions[key]:
                    action()
        else:
            if mouse_just_pressed[-(key+1)]:
                for action in self.k_down_actions[key]:
                    action()
    
    for key in self.k_up_actions.keys():
        if key not in pygut.const.MOUSE_KEYS:
            if just_released[key]:
                for action in self.k_up_actions[key]:
                    action()
        else:
            if mouse_just_released[-(key+1)]:
                for action in self.k_up_actions[key]:
                    action()
    
    for key in self.k_held_actions.keys():
        if key not in pygut.const.MOUSE_KEYS:
            if pressed[key]:
                for action in self.k_held_actions[key]:
                    action()
        else:
            if mouse_pressed[-(key+1)]:
                for action in self.k_held_actions[key]:
                    action()
