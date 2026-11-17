import pygame
import pygut.base
import pygut.collider

Element = pygut.base.Element
Timer = pygut.base.Timer
Collider = pygut.collider.Collider

app = None
_timers: list[pygut.base.Timer] = []
def add_timer(t: pygut.base.Timer):
    _timers.append(t)

K_PRESSED = 0
K_RELEASED = 1
K_HELD = 2

M1: int = 0
M2: int = 1
M3: int = 2
M4: int = 3
M5: int = 4

class Application:
    '''Basic application window. Shows an optional start_screen on startup.'''
    def __init__(self, screen_size: tuple[int, int] = (640,480), title: str = 'Pygame Window', fps: int = 60, resizable: bool = True, maximize: bool = False, handle_init: bool = True, handle_bg: bool = True):
        global app
        if handle_init:
            pygame.init()
        
        self.win = pygame.Window(title, screen_size, resizable=resizable, maximized=maximize)
        self.base_size = self.win.size
        self.center = (self.base_size[0]/2, self.base_size[1]/2)
        self.draw_to = self.win.get_surface()
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.handle_bg = handle_bg
        
        self.screen = None
        
        app = self
       
    def update(self, **kwargs):
        '''Called once per frame. By default updates all of the entities in self.screen as well as count down all of its timers.
           Override in a subclass to add extra functionality.'''
        if not self.screen is None:
            self.screen.update(**kwargs)
        
        for t in _timers:
            t.countdown(kwargs['dt'])
    
    def _step(self, dt: float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if self.screen is not None:
            self.update(dt=dt, game_elements=self.screen.game_elements, ui_elements=self.screen.ui_elements)
            if self.handle_bg: self.draw_to.blit(self.screen, (0,0))
            self.screen.elements.draw(self.draw_to)
            self.win.flip()
        else:
            self.draw_to.fill((0, 0, 0))
            self.win.flip()

    def run(self):
        '''Runs the game loop. Framerate is set to whatever was specified on object creation. Calls pygame.quit() when the loop ends.'''
        while self.running:
            dt = 1 / self.fps
            self._step(dt)
        
            self.clock.tick(self.fps)
            
        pygame.quit()
        
    def set_screen(self, screen: pygut.base.Screen):
        self.screen = screen