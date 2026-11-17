import pygame

class Collider:
    '''Base hitbox object to store the position of an object. Subclasses can add functionality such as a physics engine.
       x,y is the center of the object.'''
    def __init__(self, x: float, y: float):
        self.pos = pygame.Vector2(x, y)
    
    def collides(self, other: 'Collider') -> bool: ...
        
    def move(self, dist):
        self.pos += dist

class RectCollider(Collider):
    def __init__(self, x: float, y: float, w: float, h: float):
        super().__init__(x, y)
        
        self.bounds = pygame.Rect(x - w/2, y - h/2, w, h)
        
    def move(self, dist):
        super().move(dist)
        self.bounds.move_ip(dist)
    
    def collides(self, other: Collider):
        if isinstance(other, RectCollider):
            return self.bounds.colliderect(other.bounds)