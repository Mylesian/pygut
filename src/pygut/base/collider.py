import pygame
from base import Collider

class RectCollider(Collider):
    def __init__(self, x: float, y: float, w: float, h: float):
        super().__init__(x, y)
        
        self.bounds = pygame.Rect(x - w/2, y - h/2, w, h)
        
    def _truncated_line(self, other: Collider) -> pygame.Vector2:
        vect = other.pos - self.pos
        line = self.bounds.clipline(self.pos.x, self.pos.y, vect.x, vect.y)
        
        return pygame.math.Vector2(line[1][0] - line[0][0], line[1][1] - line[0][1]) # type: ignore
    
class CircleCollider(Collider):
    def __init__(self, x: float, y: float, r: float):
        super().__init__(x, y)
        self.r = r

    def _truncated_line(self, other: Collider) -> pygame.Vector2:
        vect = other.pos - self.pos
        vect.scale_to_length(self.r)
        
        return vect