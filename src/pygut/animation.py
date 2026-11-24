from types import FunctionType
from typing import Collection, Union
import pygame
from pygut.base import Point
from pygut._internal import convert_point

class Animation:
    '''Class to store information and update an animated Surface.'''
    def __init__(self, frames: Collection[pygame.Surface], start_pos: int = 0, on_finish: FunctionType | None = None):
        self.frames = frames
        self.on_finish = on_finish
        
        self.pointer = frames[start_pos]
        self.pointer_pos = start_pos
        
    def next(self):
        self.current_frame_pos += 1
        if self.current_frame_pos >= len(self.frames):
            if self.loop: 
                self.current_frame_pos = 0
            else:
                if isinstance(self.on_finish, FunctionType): self.on_finish()
                return
        
        self.current_frame = self.frames[self.current_frame_pos]

SheetLike = Union[pygame.Surface, str]

class SpriteSheet:
    def __init__(self, sheet: SheetLike, sheet_frame_dimensions: Point, final_frame_dimensions: Point, frame_offset: Point):
        convert_point(sheet_frame_dimensions)
        convert_point(final_frame_dimensions)
        convert_point(frame_offset)
        if isinstance(sheet, str):
            sheet = pygame.image.load(sheet).convert_alpha()
            
        x, y = frame_offset[0], frame_offset[1]
        
        self.sheet = sheet
        self.frames = []
        
        while x < sheet.get_width() - sheet_frame_dimensions[0]:
            while y < sheet.get_height() - sheet_frame_dimensions[1]:
                self.frames.append(sheet.subsurface((x, y), (sheet_frame_dimensions)))
                
                y += sheet_frame_dimensions + frame_offset[1]
            
            x += sheet_frame_dimensions + frame_offset[0]
            
def flip_frames(frames: Collection[pygame.Surface], flip_x: bool, flip_y: bool):
    for f in frames:
        f = pygame.transform.flip(f, flip_x, flip_y)
